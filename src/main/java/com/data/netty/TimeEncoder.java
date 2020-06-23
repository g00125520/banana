package com.data.netty;

import org.apache.hbase.thirdparty.io.netty.buffer.ByteBuf;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelHandlerContext;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelOutboundHandlerAdapter;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelPromise;
import org.apache.hbase.thirdparty.io.netty.handler.codec.MessageToByteEncoder;

public class TimeEncoder extends ChannelOutboundHandlerAdapter{

    @Override
    public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {
        UnixTime m = (UnixTime) msg;
        ByteBuf encoded = ctx.alloc().buffer(4);
        encoded.writeInt((int)m.value());
        ctx.write(encoded, promise);
    }

    public class TimeEn extends MessageToByteEncoder<UnixTime>{

        @Override
        protected void encode(ChannelHandlerContext ctx, UnixTime msg, ByteBuf out) throws Exception {
            out.writeInt((int) msg.value());
        }
    }
    
}