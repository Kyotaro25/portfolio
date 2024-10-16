package com.example.nitaku.form;

import java.time.LocalDate;

import org.springframework.data.annotation.Transient;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Component;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Component
@NoArgsConstructor
@AllArgsConstructor
public class RegistrationForm {
	
	//登録する時に必要な項目
	//PKは自動生成
	/** 識別ID */
	private Integer id;
	
	//①名前
	@NotBlank
	private String user_name;
	//②コメント
	private String comment;
	//③回数
	//private int count;
	
	//データベースに登録する為の保持回数
	@Transient
	private int resultCount;
	//④日時(登録ボタンを押した時に取得される日時)
	@DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
	private LocalDate day;
	
	

}
