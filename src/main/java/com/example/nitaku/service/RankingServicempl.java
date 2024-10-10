package com.example.nitaku.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.nitaku.entity.Ranking;
import com.example.nitaku.repository.NitakuRepository;


@Service
@Transactional
public class RankingServicempl implements NitakuService {
	/** Repository 注入 */
	@Autowired
	NitakuRepository repository;

	@Override
	public Iterable<Ranking> selectAll() {
		// TODO 自動生成されたメソッド・スタブ
		return repository.findAll();
	}

	@Override
	public void insertRanking(Ranking rank) {
		// TODO 自動生成されたメソッド・スタブ
		repository.save(rank);

	}

	@Override
	public Iterable<Ranking> selectOrder() {
		// TODO 自動生成されたメソッド・スタブ
		return repository.getOrdercount();
	}



}

