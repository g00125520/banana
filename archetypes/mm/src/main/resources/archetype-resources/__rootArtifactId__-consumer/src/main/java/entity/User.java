package ${package}.entity;

import java.math.BigDecimal;

import lombok.Data;

@Data
public class User {
    
    public static final User DEFAULT;

    static{
        DEFAULT = new User();
        DEFAULT.setAge(-1);
        DEFAULT.setUsername("default");
        DEFAULT.setName("default");
        DEFAULT.setId(-1l);
        DEFAULT.setBalance(BigDecimal.valueOf(0.0));
    }

    private Long id;

    private String username;

    private String name;

    private Integer age;

    private BigDecimal balance;
    
}