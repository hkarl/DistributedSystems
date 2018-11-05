#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <string.h> 

#include "message_C_builder.h"

#undef ns
#define ns(x) FLATBUFFERS_WRAP_NAMESPACE(VS_wire_transfer, x)

#define c_vec_len(V) (sizeof(V)/sizeof((V)[0]))

void build_message(flatcc_builder_t *B){
    int8_t cont[] = {0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x66, 0x72, 0x6f, 0x6d, 0x20, 0x6f, 0x6c, 0x64, 0x20, 0x43, 0x2e, 0x0};
    size_t cont_count = c_vec_len(cont);

    ns(Message_start_as_root(B));
    ns(Message_header_create(B, ns(Type_PULL), 29));
    ns(Message_from_create_str(B, "C"));
    ns(Message_hasContent_add(B, 1));
    ns(Message_content_create(B, cont, cont_count));
    ns(Message_end_as_root(B));
}

void access_message_buffer(const void *buffer){
    ns(Message_table_t) m = ns(Message_as_root(buffer));

    if(m == 0){
        perror("Message not available\n");
    }

    ns(MessageHeader_struct_t) header = ns(Message_header(m));
    printf("request: %s\n", ns(Type_name(ns(MessageHeader_request(header)))));
    printf("seq_num: %d\n", ns(MessageHeader_seq_num(header)));

    flatbuffers_string_t from = ns(Message_from(m));
    size_t from_len = flatbuffers_string_len(from);
    printf("from len: %zu\n", from_len);
    printf("from: %s\n", from);

    flatbuffers_bool_t hasContent = ns(Message_hasContent(m));
    printf("hasContent: %u\n", hasContent);

    flatbuffers_int8_vec_t content = ns(Message_content(m));
    size_t content_len = flatbuffers_int8_vec_len(content);
    printf("content len: %zu\n", content_len);
    // Interpret int8_t as char for the sake of this example
    printf("content: %s\n", content);
}

int main(){
    int sockfd;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == -1){
        perror("Could not create socket\n");    
        exit(1);    
    }    
    
    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons(9999);

    if(connect(sockfd, (struct sockaddr *)&server , sizeof(server)) < 0){
        perror("Could not create socket\n");    
        exit(1);     
    }

    size_t received_size = 0;
    char rbuf[1024];
    memset(rbuf, 0, 1024);
    received_size = read(sockfd, rbuf, 1024);
    printf("Received bytes: %zu\n", received_size);

    access_message_buffer(rbuf);
    

    // Create a `FlatBufferBuilder`
    flatcc_builder_t builder;
    void* wbuf;
    size_t size = 0;

    // Initialize the builder object.
    flatcc_builder_init(&builder);

    build_message(&builder);

    wbuf = flatcc_builder_finalize_aligned_buffer(&builder, &size);
    write(sockfd, wbuf, size);
    close(sockfd);
    flatcc_builder_aligned_free(wbuf);
    printf("Send bytes: %zu\n", size);

    return 0;
}
