package com.data.netty;

import java.util.Date;

import org.apache.hbase.thirdparty.io.netty.buffer.ByteBuf;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelHandlerContext;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelInboundHandlerAdapter;

public class TimeClientHandler extends ChannelInboundHandlerAdapter{

    private ByteBuf buf;


    @Override
    public void handlerAdded(ChannelHandlerContext ctx) throws Exception {
        buf = ctx.alloc().buffer(4);
    }

    @Override
    public void handlerRemoved(ChannelHandlerContext ctx) throws Exception {
        buf.release();
        buf = null;
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        // ByteBuf m = (ByteBuf) msg;
        // buf.writeBytes(m);
        // m.release();

        UnixTime m = (UnixTime) msg;
        System.out.println(m);
        ctx.close();

        // try {
        //     if (buf.readableBytes() >= 4) {
        //         long time = (m.readUnsignedInt() - 2208988800L) * 1000L;
        //         System.out.println(new Date(time));
        //         ctx.close();
        //     }
        // } catch (Exception e) {
        //     e.printStackTrace();
        // }
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        cause.printStackTrace();
        ctx.close();
    }

}