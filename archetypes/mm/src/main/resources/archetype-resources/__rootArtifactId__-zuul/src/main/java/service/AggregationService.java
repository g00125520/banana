package ${package}.service;

import ${package}.entity.User;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import rx.Observable;
import rx.Observer;
import rx.observables.SyncOnSubscribe;

@Service
public class AggregationService {

    @Autowired
    private RestTemplate restTemplate;


    @HystrixCommand(fallbackMethod = "defaultUser")
    public Observable<User> getUserById(Long id){
        return Observable.create(new SyncOnSubscribe<Boolean, User>(){

			@Override
			protected Boolean generateState() {
				return Boolean.TRUE;
			}

			@Override
			protected Boolean next(Boolean state, Observer<? super User> observer) {
                User user = restTemplate.getForObject("http://user-provider-h2/{id}", 
                                                        User.class, id);
                observer.onNext(user);
                observer.onCompleted();
				return generateState();
			}
           
        });
    }

    @HystrixCommand(fallbackMethod = "defaultUser")
    public Observable<User> getConsumeUserById(Long id){
        return Observable.create(new SyncOnSubscribe<Boolean, User>(){

			@Override
			protected Boolean generateState() {
				return Boolean.TRUE;
			}

			@Override
			protected Boolean next(Boolean state, Observer<? super User> observer) {
                User user = restTemplate.getForObject("http://user-consumer-h2/f/{id}", 
                                                        User.class, id);
                observer.onNext(user);
                observer.onCompleted();
				return generateState();
			}
           
        });
    }


    public User defaultUser(Long id){
        return new User();
    }
    
}