package com.data.netty;

import java.util.List;

import org.apache.hbase.thirdparty.io.netty.buffer.ByteBuf;
import org.apache.hbase.thirdparty.io.netty.channel.ChannelHandlerContext;
import org.apache.hbase.thirdparty.io.netty.handler.codec.ReplayingDecoder;

public class LiveDecoder extends ReplayingDecoder<LiveDecoder.LiveState> {
    public enum LiveState {
        LENGTH, CONTENT
    }

    public class LiveMessage {
        private String content;
        private int length;

        public String getContent() {
            return content;
        }

        public int getLength() {
            return length;
        }

        public void setLength(int length) {
            this.length = length;
        }

        public void setContent(String content) {
            this.content = content;
        }
    }

    private LiveMessage message = new LiveMessage();

    @Override
    protected void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) throws Exception {
        switch(state()){
            case LENGTH:
                int len = in.readInt();
                if (len > 0) {
                   checkpoint(LiveState.CONTENT); 
                } else {
                    out.add(message);
                }
            case CONTENT:
                byte[] bytes = new byte[message.getLength()];
                in.readBytes(bytes);
                String content = new String(bytes);
                message.setContent(content);
                out.add(message);
                break;
            default:
                throw new IllegalStateException("invalid state:" + state());
        }
    }
}