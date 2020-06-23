package com.data.netty;

// import org.apache.hbase.thirdparty.io.netty.buffer.ByteBuf;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelFuture;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelFutureListener;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelHandlerContext;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelInboundHandlerAdapter;

public class TimeServerHandler extends ChannelInboundHandlerAdapter{

    @Override
    public void channelActive(final ChannelHandlerContext ctx){
        // final ByteBuf time = ctx.alloc().buffer(4);
        // time.writeInt((int)(System.currentTimeMillis() / 1000L));

        // final ChannelFuture f = ctx.writeAndFlush(time);
        // f.addListener(new ChannelFutureListener(){
        
        //     @Override
        //     public void operationComplete(ChannelFuture future) throws Exception {
        //         assert f == future;
        //         ctx.close();
        //     }
        // });
        ChannelFuture f = ctx.writeAndFlush(new UnixTime());
        f.addListener(ChannelFutureListener.CLOSE);
    }
    
}