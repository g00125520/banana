package ${package}.controller;

import java.util.HashMap;

import ${package}.entity.User;
import ${package}.service.AggregationService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.async.DeferredResult;

import rx.Observable;
import rx.Observer;

@RestController
public class AggregationController {
    public static final Logger LOGGER = LoggerFactory.getLogger(AggregationController.class);
    
    @Autowired
    private AggregationService aggregationService;


    @GetMapping("/agg/{id}")
    public DeferredResult<HashMap<String, User>> aggregate(@PathVariable Long id){
        Observable<HashMap<String, User>> details = Observable.zip(
            aggregationService.getUserById(id), 
            aggregationService.getConsumeUserById(id),
            (user, consumerUser) -> {
                HashMap<String, User> hashMap = new HashMap<>();
                hashMap.put("user", user);
                hashMap.put("consumerUser", consumerUser);
                return hashMap;
            });
        
        return toDeferredResult(details);
    }

    public DeferredResult<HashMap<String, User>> toDeferredResult(Observable<HashMap<String, User>> details){
        DeferredResult<HashMap<String, User>> result = new DeferredResult<HashMap<String, User>>();

        details.subscribe(new Observer<HashMap<String, User>>(){

            @Override
            public void onCompleted() {
                LOGGER.debug("completed.");
            }

            @Override
            public void onError(Throwable e) {
                LOGGER.error("Error:", e);
            }

            @Override
            public void onNext(HashMap<String, User> t) {
                result.setResult(t);
            }
            
        });
        return result;
    }
}