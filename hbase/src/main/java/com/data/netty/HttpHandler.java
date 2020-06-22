package com.data.netty;

import org.apache.hbase.thirdparty.io.netty.buffer.Unpooled;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelHandlerContext;
import org.apache.hbase.thirdparty.io.netty.channel.SimpleChannelInboundHandler;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.DefaultFullHttpResponse;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.FullHttpRequest;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpHeaderNames;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpHeaderValues;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpHeaders;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpResponseStatus;
import org.apache.hbase.thirdparty.io.netty.handler.codec.http.HttpVersion;
import org.apache.hbase.thirdparty.io.netty.util.AsciiString;

public class HttpHandler extends SimpleChannelInboundHandler<FullHttpRequest> {

    private AsciiString contentType = HttpHeaderValues.TEXT_PLAIN;

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, FullHttpRequest msg) throws Exception {
        System.out.println("class:" + msg.getClass().getName());
        DefaultFullHttpResponse response = new DefaultFullHttpResponse(
            HttpVersion.HTTP_1_1, 
            HttpResponseStatus.OK,
            Unpooled.wrappedBuffer("test".getBytes()));
        
        HttpHeaders headers = response.headers();
        headers.add(HttpHeaderNames.CONTENT_TYPE, contentType + ";charset=UTF-8");
        headers.add(HttpHeaderNames.CONTENT_LENGTH, response.content().readableBytes());
        headers.add(HttpHeaderNames.CONNECTION, HttpHeaderValues.KEEP_ALIVE);

        ctx.write(response);
    }
    
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        System.out.println("channel read complete.");
        super.channelReadComplete(ctx);
        ctx.flush();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause){
        System.out.println("exception caught.");
        if(null != cause) cause.printStackTrace();
        if(null != ctx) ctx.close();
    }
}