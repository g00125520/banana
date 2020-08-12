package ${package}.config;

import ${package}.annotation.ExcludeFromComponetScan;
import com.netflix.client.config.IClientConfig;
import com.netflix.loadbalancer.IRule;
import com.netflix.loadbalancer.RandomRule;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 不能包含在主应用程序上下文的@ComponentScan中，否则该类中的配置会被
 * 所有的@RibbonClient共享。
 * 如果只想自定义某一个Ribbon客户端配置，应显式指定@ComponentScan不扫描
 * @Configuration类所在的包。
 */
@Configuration
@ExcludeFromComponetScan
public class RibbonConfig {

    @Bean
    public IRule ribbonRule(IClientConfig config){
        return new RandomRule();
    }
    
}