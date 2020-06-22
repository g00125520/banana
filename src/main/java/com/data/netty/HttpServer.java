package com.data.netty;

import org.apache.hbase.thirdparty.io.netty.bootstrap.ServerBootstrap;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelInitializer;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelOption;
import org.apache.hbase.thirdparty.io.netty.channel.nio.NioEventLoopGroup;
import org.apache.hbase.thirdparty.io.netty.channel.socket.SocketChannel;
import org.apache.hbase.thirdparty.io.netty.channel.socket.nio.NioServerSocketChannel;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpRequestDecoder;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpResponseEncoder;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpObjectAggregator;

public class HttpServer{
    private final int port;

    public HttpServer(int port){
        this.port = port;
    }

    public static void main(String[] args) throws InterruptedException {
        int port = Integer.parseInt(args[0]);
        HttpServer hs = new HttpServer(port);
        hs.start();
    }

    public void start() throws InterruptedException {
        ServerBootstrap sb = new ServerBootstrap();
        NioEventLoopGroup ne = new NioEventLoopGroup();

        sb.group(ne)
            .channel(NioServerSocketChannel.class)
            .childHandler(new ChannelInitializer<SocketChannel>() {

				@Override
				protected void initChannel(SocketChannel ch) throws Exception {
                    ch.pipeline()
                        .addLast("decoder", new HttpRequestDecoder())
                        .addLast("encode", new HttpResponseEncoder())
                        .addLast("aggregator", new HttpObjectAggregator(512 * 1024))
                        .addLast("handler", new HttpHandler());
				}
            })
            .option(ChannelOption.SO_BACKLOG, 128)
            .childOption(ChannelOption.SO_KEEPALIVE, Boolean.TRUE);
        
        sb.bind(port).sync();
    }
}