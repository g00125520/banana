package ${package}.feign;

import ${package}.config.FeignConfiguration;
import ${package}.entity.User;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;

import feign.Param;
import feign.RequestLine;
import feign.hystrix.FallbackFactory;

/**
 * 需设置：feign.hystrix.enabled: true，默认关闭。
 * https://github.com/spring-cloud/spring-cloud-netflix/issues/1277
 */
@FeignClient(name = "user-provider-h2" , 
             configuration = FeignConfiguration.class,
             //fallback = UserFeignClientFallback.class,
             fallbackFactory = UserFeignClientFallbackFactory.class)
public interface UserFeignClient {

    //@RequestMapping(value = "/{id}", method = RequestMethod.GET)
    //public User findById(@PathVariable("id") Long id);
    
    @RequestLine("GET /{id}")
    public User findById(@Param("id") Long id);
}

@Component
class UserFeignClientFallback implements UserFeignClient{

    @Override
    public User findById(Long id) {
        return User.DEFAULT;
    }
    
}

@Component
class UserFeignClientFallbackFactory implements FallbackFactory<UserFeignClient>{
    private static final Logger LOGGER = LoggerFactory.getLogger(UserFeignClientFallbackFactory.class);

    @Override
    public UserFeignClient create(Throwable cause) {
        return new UserFeignClient(){

            @Override
            public User findById(Long id) {
                LOGGER.debug("fallback cause:", cause);
                return User.DEFAULT;
            }

        };
    }
    
}