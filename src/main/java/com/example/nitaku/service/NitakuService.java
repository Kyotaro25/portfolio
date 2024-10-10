package com.example.nitaku.service;

import com.example.nitaku.entity.Ranking;

/** Quizサービス処理：Service */
public interface NitakuService {
	/** ランキング情報を全件取得 */
	Iterable<Ranking> selectAll();
	
	/** ランキングに登録 */
	void insertRanking(Ranking rank);
	
	/** ランキングを順位に並び替え */
	Iterable<Ranking> selectOrder();

}
