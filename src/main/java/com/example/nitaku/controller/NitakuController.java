package com.example.nitaku.controller;

import java.time.LocalDate;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.SessionAttributes;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.example.nitaku.entity.Ranking;
import com.example.nitaku.form.RegistrationForm;
import com.example.nitaku.service.NitakuService;

@Controller
@SessionAttributes("hitCount")
public class NitakuController {

	@Autowired
	NitakuService service;

	@Autowired
	RegistrationForm registrationForm;
	
	 // フォームの初期化メソッド
	@ModelAttribute("registrationForm")
	public RegistrationForm setUpForm() {
		return new RegistrationForm();// 新しいRegistrationFormを返す
	}

	

	@ModelAttribute("hitCount")
	public Integer hitCount() {
		return 0; // 成功回数の初期値
	}

	private boolean isLeftImageCorrect() {
		// ランダムに当たりを決定（例: 50%の確率で左が当たり）
		return Math.random() < 0.5;
	}

	@GetMapping("/game/left")
	public String leftImageClick(@ModelAttribute("hitCount") Integer hitCount, Model model,
			RedirectAttributes redirectAttributes) {
		if (isLeftImageCorrect()) {
			//正解音を鳴らす
			hitCount++; // 当たりの場合、カウントを増加
		} else {
			//カウントリセット前にredirectAttributes.addFlashAttributeで保持させる
			//引数に, RedirectAttributes redirectAttributesを渡しておく
			redirectAttributes.addFlashAttribute("resultCount", hitCount);
			//recordCount = hitCount;
			//ここまでその処理
			hitCount = 0; // ハズレの場合、カウントをリセット
			model.addAttribute("hitCount", hitCount);
			return "redirect:/result"; // リザルト画面へ遷移
		}
		model.addAttribute("hitCount", hitCount);
		return "redirect:/game"; // ゲーム画面に戻る
	}

	@GetMapping("/game/right")
	public String rightImageClick(@ModelAttribute("hitCount") Integer hitCount, Model model,
			RedirectAttributes redirectAttributes) {
		if (!isLeftImageCorrect()) { // 右が正解の場合
			//正解音を鳴らす
			hitCount++; // 当たりの場合、カウントを増加
		} else {
			//カウントリセット前にredirectAttributes.addFlashAttributeで保持させる
			//引数に, RedirectAttributes redirectAttributesを渡しておく
			redirectAttributes.addFlashAttribute("resultCount", hitCount);
			hitCount = 0; // ハズレの場合、カウントをリセット
			model.addAttribute("hitCount", hitCount);
			return "redirect:/result"; // リザルト画面へ遷移
		}
		model.addAttribute("hitCount", hitCount);
		return "redirect:/game"; // ゲーム画面に戻る
	}

	@GetMapping("/result")
	public String showResult(@ModelAttribute("hitCount") Integer hitCount, Model model) {
		model.addAttribute("hitCount", hitCount);
		model.addAttribute("registrationForm", new RegistrationForm());
		return "result";
	}

	@PostMapping("/register")
	public String registerResult(@Validated RegistrationForm form, @ModelAttribute("hitCount") Integer hitCount,
			BindingResult bindingResult, RedirectAttributes redirectAttributes) {
		form.setHitCount(hitCount); // 成功回数をフォームに設定
		
		// DBに名前が登録されているか確認する
		String name = form.getUser_name();
		Optional<Ranking> rank = service.selectOneByName(name);
		

		//ranking.setCount(form.getHitCount());
		
		//resultCountの方を使う
		// resultCountの値をcountにセット


		//入力チェック
		
		if(rank.isEmpty()) {		
		  if (!bindingResult.hasErrors()) {
			  Ranking ranking = new Ranking();
				ranking.setUser_name(name);
				ranking.setComment(form.getComment());				
			    ranking.setCount(form.getResultCount());			    
			    LocalDate d = LocalDate.now();
				ranking.setDay(d);
				
			  service.insertRanking(ranking); // データベースに保存
			  redirectAttributes.addFlashAttribute("msg","登録完了!");
			  return "redirect:/ranking";
		  } else {
			  //エラーの時は再度登録画面を表示
			
		  	  return "redirect:/result";
		  }
		} else {
			// DBにユーザーがある場合の処理
			Ranking userGet = rank.get(); // ユーザーを取ってくる
			
			// 回数を比較し、記録更新していたらデータベースを更新
			if(form.getResultCount() > userGet.getCount()) {
				userGet.setCount(form.getResultCount());
				userGet.setComment(form.getComment());
			    LocalDate d = LocalDate.now();
				userGet.setDay(d);
				
				service.updateRanking(userGet);
				redirectAttributes.addFlashAttribute("msg","記録更新！");
				
				return "redirect:/ranking";
			} else {
				redirectAttributes.addFlashAttribute("msg","記録更新ならず・・・");
				return "redirect:/ranking";
			}
			
			
			}
		}

	
	
	
	
	
	

	@GetMapping("/top")
	public String showTop() {
		return "top";
	}

	@GetMapping("/game")
	public String showGame(@ModelAttribute("hitCount") Integer hitCount, Model model) {
		return "game";
	}
	@GetMapping("/ranking")
	public String showRanking(Model model) {
		Iterable<Ranking> list = service.selectOrder();
		model.addAttribute("list",list);
		
		return "ranking";
	}
	
	
}
