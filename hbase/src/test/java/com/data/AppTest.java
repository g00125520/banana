package com.data;

import static org.junit.Assert.assertTrue;

import com.data.hbase.HbaseUtils;

import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    /**
     * Rigorous Test :-)
     */
    @Test
    public void shouldAnswerWithTrue()
    {
        HbaseUtils.doNothing();
        assertTrue( true );
    }
}
