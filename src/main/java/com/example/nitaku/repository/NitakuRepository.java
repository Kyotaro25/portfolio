package com.example.nitaku.repository;

import java.util.Optional;

import org.springframework.data.jdbc.repository.query.Query;
import org.springframework.data.repository.CrudRepository;

import com.example.nitaku.entity.Ranking;


/** Rankingテーブル:RepositoryImpl */
public interface NitakuRepository extends CrudRepository<Ranking, Integer>{
@Query("SELECT user_name, comment, count, day FROM Ranking ORDER BY count DESC")	
	Iterable<Ranking> getOrdercount();

@Query("SELECT * FROM Ranking WHERE user_name = :name")
		Optional<Ranking> findUserByName(String name);

@Query("SELECT count FROM Ranking WHERE user_name = :name")
        Optional<Ranking> findUserByCount(int count);



}

