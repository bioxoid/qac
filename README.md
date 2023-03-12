## Get Started
```zsh
git clone https://github.com/bioxoid/qac
cd qac && npm i
npm run dev
```
src/routes/+page.svelteが星座のページ

## URL
| URL | description |
| --- | ---         |
| / | 星座           |
|/myth| ChatGPTによる神話生成|
|/about|aboutページ|


## ToDo
- [ ] hoverで星座名、有名な星表示
- [ ] 描画範囲指定のui(誕生日とか入れたい星とか)
- [ ] お絵描きを画像として保存してファイル名で管理するか、宇宙ごとにjsonで`星座名:お絵描きのdataurl`で管理する。それか宇宙ごとに1枚のテクスチャにどんどん追加してってその画像を保存する
- [ ] 地軸と地面追加、下向けないように
- [ ] canvas:消しゴム、全消し、データ送信時に領域指定してもらう、undo
- [ ] 星座n個ごとに新たな宇宙生成、ユーザーが宇宙を選択可能にする？
- [ ] 英語対応(i18n)
- [ ] モバイルとか対応
- [ ] ローディングアニメーション
- [ ] マウスがcanvas外に出た時の処理
- [ ] リサイズ
- [x] 神話、ChatGPTか人かコンビ

## めも
<https://zenn.dev/karno/articles/091f9f23dab30c#>  
<https://github.com/Stellarium/stellarium>

## 案
星座線を[fat line](https://github.com/mrdoob/three.js/blob/master/examples/webgl_lines_fat.html)に?  
ローディングページ: いらすとやから適当に20枚くらい拾ってきて星座にしたやつを、before,afterみたいにする  