#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <uv.h>

typedef int (*cmd_handler)(uv_buf_t* buf);

uv_loop_t* loop;

#define MAX_COUNTER 1000000
uint64_t* COUNTERS;
int is_dumping = 0;

int read_counter_number (uv_buf_t* buf, int offset, int* counter) {
	if (sscanf(buf->base+offset, "%u", counter) == 1
		&& *counter < MAX_COUNTER) return 1;
	buf->len = snprintf (buf->base, buf->len, "WRONG COUNTER\n");
	return 0;
}

void print_counter (uv_buf_t* buf, int counter) {
	buf->len = snprintf (buf->base, buf->len, "%lu\n", COUNTERS[counter]);
}

int cmd_get (uv_buf_t* buf) {
	int cnt;
	if (read_counter_number (buf, 3, &cnt))
		print_counter (buf, cnt);
	return 0;
}

int cmd_increment (uv_buf_t* buf) {
	int cnt;
	if (read_counter_number (buf, 3, &cnt)) {
		COUNTERS[cnt]++;
		print_counter (buf, cnt);
	}
	return 0;
}

void do_dump () {
	is_dumping = 1;
	if (fork()) {
		fprintf(stderr, "DUMP started\n");	
	} else {
		FILE* f;
		fprintf(stderr, "Opening dump file\n");
		f = fopen("counter.dump", "w++");
		if (!f) {
			fprintf(stderr, "Cannot open dump file\n"); 
			exit(1);
		}
		
		int i;
		fprintf(stderr, "SLEEPING...\n");
	
		fprintf(stderr, "DUMPING...\n");
		for (i = 0; i < MAX_COUNTER; i++) {
			//if (COUNTERS[i])
				fprintf(f, "%d %ld\n", i, COUNTERS[i]);
		}
		fprintf(stderr, "DUMP done\n");
		fclose(f);
		exit(0);
	}
}

int cmd_decrement (uv_buf_t* buf) {
	int cnt;
	if (read_counter_number (buf, 3, &cnt)) {
		COUNTERS[cnt]--;
		print_counter (buf, cnt);
	}
	return 0;
}

int cmd_zero (uv_buf_t* buf) {
	int cnt;
	if (read_counter_number (buf, 4, &cnt)) {
		COUNTERS[cnt] = 0;
		print_counter (buf, cnt);
	}
	return 0;
}

int cmd_quit (uv_buf_t* buf) {
	buf->len = snprintf (buf->base, buf->len, "GOOD BYE!\n");
	return 1;
}

int cmd_dump (uv_buf_t* buf) {
	if (!is_dumping) {
		do_dump();
		buf->len = snprintf(buf->base, buf->len, "DUMP is starting\n");
	} else {
		buf->len = snprintf(buf->base, buf->len, "DUMP is already started\n");
	}
	return 0;
}

struct _command {
	char name[8];
	cmd_handler handler;
};

struct _command COMMANDS[] = {
	{"INC", cmd_increment},
	{"DEC", cmd_decrement},
	{"ZERO", cmd_zero},
	{"GET", cmd_get},
	{"QUIT", cmd_quit},
	{"DUMP", cmd_dump},
//	{"REGDUMPSTART", cmd_regstart},
//	{"REGDUMPFIN", cmd_regfinish},
	{"", NULL}
};

int process_userinput (ssize_t nread, uv_buf_t* buf) {
	struct _command* cmd;
	for (cmd = COMMANDS; cmd->handler; cmd++) {
		if (!strncmp (buf->base, cmd->name, strlen (cmd->name))) {
			return cmd->handler(buf);
		}
	}
	
	buf->len = snprintf (buf->base, buf->len, "UNKNOWN COMMAND '%3s'\n", buf->base);
	return 0;
}

void alloc_buffer (uv_handle_t* handle, size_t suggested_size, uv_buf_t* buf) {
	buf->base = uv_handle_get_data(handle);
	buf->base = (char*)realloc(buf->base, suggested_size);
	buf->len = suggested_size;
	uv_handle_set_data(handle, buf->base);
}

void on_conn_close (uv_handle_t* client) {
	void* buf = uv_handle_get_data(client);
	if (buf) {
		fprintf(stderr, "Freeing buf\n");
		free(buf);
	}
	fprintf(stderr, "Freeing client\n");
	free(client);
}

void on_conn_write (uv_write_t* req, int status) {
	if (status) {
		fprintf (stderr, "Write error: %s\n", uv_strerror(status));
	}
	free(req);
}

void on_client_read (uv_stream_t* client, ssize_t nread, const uv_buf_t* buf) {
	if (nread < 0) {
		if (nread != UV_EOF) {
			fprintf (stderr, "Read error %s\n", uv_err_name(nread));
			uv_close ((uv_handle_t*)client, on_conn_close);	
		}
	} else if (nread > 0) {
		int res;
		uv_buf_t wrbuf = uv_buf_init (buf->base, buf->len);
		res = process_userinput (nread, &wrbuf);
		
		uv_write_t* req = (uv_write_t*)malloc(sizeof(uv_write_t));
		uv_write(req, client, &wrbuf, 1, on_conn_write);
		
		if (res) {
			uv_close ((uv_handle_t*)client, on_conn_close);
		}
	}
}

void on_new_connection (uv_stream_t* server, int status) {
	if (status < 0) {
		fprintf (stderr, "New connection error %s\n", uv_strerror(status));
		return;
	}
	
	uv_tcp_t *client = (uv_tcp_t*)malloc(sizeof(uv_tcp_t));
	bzero(client, sizeof(uv_tcp_t));
	uv_tcp_init(loop, client);
	
	if (uv_accept(server, (uv_stream_t*)client) == 0) {
		fprintf(stderr, "Client %p connected\n", client);
		uv_read_start((uv_stream_t*)client, alloc_buffer, on_client_read);
	} else {
		fprintf(stderr, "Error while accepting\n");
		uv_close((uv_handle_t*)client, on_conn_close);
	}
}

void on_sig_child (uv_signal_t* handle, int signum) {
	int status;
	fprintf(stderr, "SIGCHLD got with %d\n", signum);
	if (waitpid(-1, &status, WNOHANG) > 0) {
		fprintf(stderr, "CHILD process has exit status %d\n", status);
		is_dumping = 0;
	} else {
		fprintf(stderr, "Nothing changed\n");
	}
}

int main () {
	int result;
	struct sockaddr_in addr;
	
	loop = uv_default_loop();
	COUNTERS = calloc(sizeof(uint64_t), MAX_COUNTER);
	uv_tcp_t server;
	uv_tcp_init(loop, &server);
	uv_ip4_addr("0.0.0.0", 7000, &addr);
	uv_tcp_bind (&server, (const struct sockaddr*)&addr, 0);
	uv_signal_t childhandler;
	uv_signal_init(loop, &childhandler);
	uv_signal_start(&childhandler, on_sig_child, SIGCHLD);	
	
	int r = uv_listen((uv_stream_t*)&server, 1024, on_new_connection);
	if (r) {
		fprintf(stderr, "Listen errror %s\n", uv_strerror(r));
		return 1;
	}
	
	result = uv_run(loop, UV_RUN_DEFAULT);
	
	fprintf(stderr, "Finalization...\n");
	free(COUNTERS);
	
	return result;
}
