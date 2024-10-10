package com.example.nitaku.entity;

import java.time.LocalDate;

import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.format.annotation.DateTimeFormat;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Ranking {
	/** ID */
	@Id
	private Integer id;
	/** 名前 */
	private String user_name;
	/** コメント */
	private String comment;
	/** 回数 */
	private Integer count;
	
	/** 登録用の保持回数 */
	// このフィールド↓がデータベースの'count'に保存される
	@Transient
	private Integer resultCount;
	/** 日付 */
	@DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
	private LocalDate day;
	
	/** a */
	
	
	

}
