package com.example.nitaku.service;

import java.util.Optional;

import com.example.nitaku.entity.Ranking;

/** Quizサービス処理：Service */
public interface NitakuService {
	/** ランキング情報を全件取得 */
	Iterable<Ranking> selectAll();
	
	/** ランキングに登録 */
	void insertRanking(Ranking rank);
	
	/** ユーザ情報を指定した名前を元に1件取得します */
	Optional<Ranking> selectOneByName(String name);
	
	/** ユーザー情報の回数を取得 */
	Optional<Ranking> selectOneByCount(int count);
		
	/** ランキングにユーザー情報を更新 */
	void updateRanking(Ranking rank);
	
	/** ランキングを順位に並び替え */
	Iterable<Ranking> selectOrder();
	
	
	

	

}
