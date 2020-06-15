package com.data;

import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptor;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptorBuilder;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.TableDescriptorBuilder;
import org.apache.hadoop.hbase.util.Bytes;

public class HbaseUtils {

    private static Connection conn;

    static {
        Configuration conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.property.clientPort", "2181");
        conf.set("hbase.zookeeper.quorum", "127.0.0.1");
        try {
            conn =  ConnectionFactory.createConnection(conf);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public static boolean createTable(String tableName, List<String> columnFamilies){
        try {
            HBaseAdmin admin = (HBaseAdmin)conn.getAdmin();
            TableName tName = TableName.valueOf(tableName);
            if(admin.tableExists(tName)){
                return false;
            }

            TableDescriptorBuilder tDescriptor = TableDescriptorBuilder.newBuilder(tName);
            columnFamilies.forEach(columnFamily -> {
                ColumnFamilyDescriptorBuilder cfb = ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes(columnFamily));
                cfb.setMaxVersions(1);
                ColumnFamilyDescriptor cdf = cfb.build();
                tDescriptor.setColumnFamily(cdf);
            });

            admin.createTable(tDescriptor.build());
        } catch (Exception e) {
            e.printStackTrace();
        }

        return true;
    }

}