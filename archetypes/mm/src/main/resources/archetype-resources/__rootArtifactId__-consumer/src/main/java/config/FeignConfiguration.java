package ${package}.config;

import ${package}.annotation.ExcludeFromComponetScan;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import feign.Contract;
import feign.Logger;

/**
 * 不能包含在主应用程序上下文的@ComponentScan中，否则该类中的配置会被
 * 所有的@RibbonClient共享。
 * 如果只想自定义某一个Ribbon客户端配置，应显式指定@ComponentScan不扫描
 * @Configuration类所在的包。
 */
@Configuration
@ExcludeFromComponetScan
public class FeignConfiguration {

    @Bean
    public Contract feignContract(){
        return new feign.Contract.Default();
    }
    
    @Bean
    public Logger.Level feignLogLevel(){
        return Logger.Level.FULL;
    }

}