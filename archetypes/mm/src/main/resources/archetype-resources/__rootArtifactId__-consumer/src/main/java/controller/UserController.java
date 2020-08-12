package ${package}.controller;

import ${package}.entity.User;
import ${package}.config.Service;
import ${package}.feign.UserFeignClient;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixProperty;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.cloud.client.loadbalancer.LoadBalancerClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;


/**
 * 
 */
@RestController
public class UserController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private DiscoveryClient discoveryClient;

    @Autowired
    private LoadBalancerClient loadBalancerClient;

    @Autowired
    private UserFeignClient userFeignClient;
    
    
    @HystrixCommand(fallbackMethod = "findByIdDefault" , commandProperties = {
        @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "1000"),
        @HystrixProperty(name = "metrics.rollingStats.timeInMilliseconds", value = "10000"),
    }, threadPoolProperties = {
        @HystrixProperty(name = "coreSize", value = "1"),
        @HystrixProperty(name = "maxQueueSize", value = "10"),
    })
    @GetMapping("/{id}")
    public User findById(@PathVariable Long id){
        return restTemplate.getForObject(Service.USER.toUrl(id.toString()), User.class);
    }

    public User findByIdDefault(Long id){
        return User.DEFAULT;
    }
   
    @GetMapping("/f/{id}")
    public User findByIdV2(@PathVariable Long id) {
        return  userFeignClient.findById(id);
    }

    @GetMapping("/user-instance")
    public List<ServiceInstance> showInfo(){
        return discoveryClient.getInstances(Service.USER.getInstance());
    }

    @GetMapping("/log-instance")
    public void logInstance(){
        loadBalancerClient.choose("serviceId");
    }
}