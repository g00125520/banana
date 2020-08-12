package ${package}.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import ${package}.entity.User;


@Repository
public interface UserRepository extends JpaRepository<User, Long>{

}