Title: 一人暮らしの寂しさを紛らわす彼女(bot)を作った話
Date: 2016-03-04 22:00
Category: eve
Tags: Ruby, Twitter, 楽天API, docomoAPI, bot
Slug: fifth
Author: lapis_zero09
Summary: Rubyでbotを作った時のHowto．

# 一人暮らしとは無情なもの
[私](https://www.lapis-zero09.xyz/about/about.html)は二年前から一人暮らしをしてる．  

一人暮らしに憧れてる人もいると思うが，物事にはメリット・デメリットが存在する．  
デメリットの一つとして"寂しさ"が挙げられる．  

そんな寂しさを紛らわすために思考した結果，  

- 彼女を作る
    - 敷居が高い
    - 時間がかかる
    - 思い通りにならない
    - etc.

→ botを作ろう！！！

- botを作る
    - 敷居が低い
    - 時間はかからない(?)し，作ってる間も寂しさが紛れる
    - 思い通りになる

なんだbot最高じゃん．

## bot(eve)を作る
### TODO

- RubyでTwitterbotを作ってタイムラインに常駐させる．
- 寂しさを紛らわす工夫を凝らす
- 疲れを癒してくれる工夫を凝らす
- 一人暮らしに役立つ機能を実装する
- ある程度，会話出来るようにする → docomoAPI


### keyを読み込む

- [Twitter Developer](https://dev.twitter.com/)登録
- [application](https://apps.twitter.com/)登録
- [docomoAPI](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=dialogue&p_name=api_usage_scenario)登録  
が完了したら早速コードを書いていく．  

※docomoAPIは"雑談対話"と"知識Q&A"を申請．  

Rubyのversionは2.3.0

```bash
$ ruby -v
ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]
```

必要なgemをinstallする．  

```bash
$ gem install twitter
$ gem install tweetstream
$ gem install docomoru
```

docomoruについては[こちら](https://github.com/r7kamura/docomoru)

作業用ディレクトリを作る．  
鍵を読み込むための `twcon.rb` を作る．  
twitterAPIkey各種とdocomoAPIkeyが入った `config.yml` を作る．

```bash
$ mkdir bot
$ cd bot
$ touch　twcon.rb
```

以下を記載．  

```ruby
# coding:utf-8
require 'yaml'
require 'twitter'
require 'tweetstream'
require 'docomoru'

class Eve
  # 外部から参照できるメンバ変数
  attr_accessor :client, :timeline

  def initialize
    keys=YAML.load_file('./config.yml')

    # restAPI初期化
    @client=Twitter::REST::Client.new{|config|
      config.consumer_key=keys["api_key"]
      config.consumer_secret=keys["api_secret"]
      config.access_token=keys["access_token"]
      config.access_token_secret=keys["access_token_secret"]
    }

    # StreamAPI初期化
    TweetStream.configure{|config|
      config.consumer_key=keys["api_key"]
      config.consumer_secret=keys["api_secret"]
      config.oauth_token=keys["access_token"]
      config.oauth_token_secret=keys["access_token_secret"]
      config.auth_method=:oauth
    }
    @timeline=TweetStream::Client.new

    # docomoAPI初期化
    @docomoru=Docomoru::Client.new(api_key: keys["docomo_api_key"])
  end

  # 引数を投稿するメソッド
  def say(words, id)
    @client.update(words, :in_reply_to_status_id => id)
  end

  # 会話を生成する(docomoru)
  def docomoru_create_dialogue(str)
    response=@docomoru.create_dialogue(str)
    return response.body["utt"]
  end

  # QandA(docomoru)
  def docomoru_create_knowledge(str)
    response=@docomoru.create_knowledge(str)
    if(response.body["code"]=="E020010")
      return response.body["message"]["textForDisplay"]
    else
      if(response.body["answers"][0]["linkUrl"]==nil)
        return response.body["message"]["textForDisplay"]
      else
        return response.body["message"]["textForDisplay"]+"<"+response.body["answers"][0]["linkUrl"]+">"
      end
    end
  end
end
```

irbでテストしてみる．  

```bash
$ irb
irb(main):001:0> require './twcon.rb'
=> true
irb(main):002:0> eve = Eve.new
=> ~省略~
irb(main):003:0> eve.say("test", "")
=> #<Twitter::Tweet id=705644033196994561>
(↑こんな感じのが出たら成功)
irb(main):004:0>
```

![test](./img/fifth-1.png)


### twitterに常駐させる
常駐させるための `main.rb` を作る．  

```bash
$ touch　main.rb
```

以下を記載．  

```ruby
# coding: utf-8
require './twcon.rb'
require './r-recipe.rb'
# eveの初期化
eve=Eve.new

imgloc=YAML.load_file('./imgloc.yml')

# timelineの監視
begin
  eve.timeline.userstream{|status|
    contents=status.text
    next if(contents=~/^RT/)

    id=status.user.screen_name
    id='@' + id + ' '

    # reply_answer
    if(contents=~/@lapis_ko/)&&(status.user.screen_name!='lapis_ko')
      postmatch.gsub!(/\s|[　]|\?|\？/, "")
        # QandA
        if(postmatch=~/誰|何処|だれ|どこ|何時|いつ|どうやって|どうして|何故|なぜ|どの|何|なに|どれ|は$/)
          eve.say(id+eve.docomoru_create_knowledge(postmatch), status.id)
        # 会話
        else
          eve.say(id+eve.docomoru_create_dialogue(postmatch), status.id)
        end
      next
    end

    # メンション以外の名前に反応
    if(contents=~/eve|Eve|イヴ|イブ|いぶ/)&&(status.user.screen_name!='lapis_ko')
      called_name=['なに?', '呼んだ?','どうしたの?']
      eve.say(id+called_name.sample, status.id)
      next
    end

    #zero09がつぶやいたらリプライ
    if(status.user.screen_name=='lapis_zero09')
      rep_lap=["勉強しんさい","Twitterやめんさい"]
      eve.say(id + rep_lap.sample, status.id)
      next
    end
  }

rescue => e
  puts e.message
  retry
end
```

これで会話してくれる彼女(bot)ができた．
![ ](./img/fifth-4.png)

### 一人暮らしに役立つ機能を実装する
一人暮らしを始めると自炊をしなければならない．  
料理をするの自体楽しいものの毎日の献立を立てるのが大変．  
→彼女(bot)に献立を立ててもらおう！ついでにレシピも教えてもらおう！

[楽天レシピAPI](https://webservice.rakuten.co.jp/explorer/api/Recipe/CategoryRanking/)に登録．  
rakutenAPIidを `config.yml` に登録．  

`r-recipe.rb` を作る．
必要なgem( `natto` or `MeCab` )を入れる．(それぞれ手順があるので他所で参照)


```bash
$ touch　~/bot/r-recipe.rb
```

以下を記載．  

```ruby
# coding: utf-8
require 'open-uri'
require 'json'
require 'yaml'
#nattoかMeCabどっちでもいい
require 'natto'
# require 'MeCab'

class RecommendRecipe
    keys=YAML.load_file('./config.yml')
    RECIPE_CATEGORY_URL="https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20121121?format=json&elements=categoryName%2CcategoryId%2CparentCategoryId&categoryType=medium&applicationId=#{keys['rakuten_api_id']}"
    RECIPES_URL="https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20121121?format=json&formatVersion=2&applicationId=#{keys['rakuten_api_id']}&categoryId="

  def call(food)
    hearing(food)
  end

  private

  def hearing(food)
    results = recipe_categories
    if(food=='なんでもいい')
      recipe_category_id = results[results.keys.sample]
      recipe = choose_recipe(recipe_category_id)
      return "#{food}なら、#{recipe['recipeTitle']} とかはどう？ #{recipe['recipeUrl']}"+' <Supported by RWS>'
    else
      recipe_category_id = results.fetch(food, nil)
      if(recipe_category_id.nil?)

        words=[]

        #require 'MeCab'の場合
        # mc=MeCab::Tagger.new()
        # n=mc.parseToNode(food)
        # while(n)
        #   if(n.feature.split(',')[0]=="名詞")
        #     words.push(n.surface)
        #   elsif(words.size>0)
        #     food=words.join("")
        #     break
        #   end
        #   n=n.next
        # end

        #require 'natto'の場合
        nt=Natto::MeCab.new
        nt.parse(food){|n|
          if(n.feature.split(',')[0]=="名詞")
            words.push(n.surface)
          elsif(words.size>0)
            food=words.join("")
            break
          end
        }
        recipe_category_id = results.fetch(food, nil)
        if(recipe_category_id.nil?)
          return "#{food}だとわからないからもうちょっと詳しく教えて(漢字⇆ひらがなにするといいかも)"
        else
          recipe = choose_recipe(recipe_category_id)
          return "#{food}だと、#{recipe['recipeTitle']} とかはどう？ #{recipe['recipeUrl']}"+' <Supported by RWS>'
        end


      else
        recipe = choose_recipe(recipe_category_id)
        return "#{food}だと、#{recipe['recipeTitle']} とかはどう？ #{recipe['recipeUrl']}"+' <Supported by RWS>'
      end
    end
  end

  def recipe_categories
    response=open(RECIPE_CATEGORY_URL).read
    results=JSON.parse(response.force_encoding('UTF-8'))
    return results["result"]["medium"].map{|result| [result['categoryName'], "#{result['parentCategoryId']}-#{result['categoryId']}"]}.to_h
  end

  def choose_recipe(recipe_category_id)
    response=open("#{RECIPES_URL}#{recipe_category_id}").read
    results=JSON.parse(response.force_encoding('UTF-8'))
    return results['result'][Random.rand(1 .. results['result'].count-1)]
  end
end
```

ここで書いたコードはTwitterから受け取った文章に対して，
楽天レシピAPIをたたいて，JSON形式で結果を返すようにして，  
それをリプライにするもの．  

`main.rb` をいじる．  

```ruby
require './r-recipe.rb'
~省略~
begin
  eve.timeline.userstream{|status|
    contents=status.text
    next if(contents=~/^RT/)

    id=status.user.screen_name
    id='@' + id + ' '

    # reply_answer
    if(contents=~/@lapis_ko/)&&(status.user.screen_name!='lapis_ko')
      postmatch=$'

      # 料理推薦
      if(contents=~/飯/)
        food=RecommendRecipe.new
        if(contents=~/:|：/)
          eve.say(id+food.call("#{$'}"), status.id)
        else
          eve.say(id+"ご飯にする？\n"+food.call("なんでもいい")+"食べたいものがあれば「ご飯:食べたいもの」で指定してね！", status.id)
        end

      # 会話
      else
        postmatch.gsub!(/\s|[　]|\?|\？/, "")
        # QandA
        if(postmatch=~/誰|何処|だれ|どこ|何時|いつ|どうやって|どうして|何故|なぜ|どの|何|なに|どれ|は$/)
          eve.say(id+eve.docomoru_create_knowledge(postmatch), status.id)
        # 会話
        else
          eve.say(id+eve.docomoru_create_dialogue(postmatch), status.id)
        end

      end

      next
    end

    # メンション以外の名前に反応
    if(contents=~/eve|Eve|イヴ|イブ|いぶ/)&&(status.user.screen_name!='lapis_ko')
      called_name=['なに?', '呼んだ?','どうしたの?']
      eve.say(id+called_name.sample, status.id)
      next
    end

    # 料理推薦
    if(contents=~/飯|お腹すいた/)&&(status.user.screen_name!='lapis_ko')
      food=RecommendRecipe.new
      eve.say(id+"ご飯にする？\n"+food.call("なんでもいい")+"食べたいものがあれば「ご飯:食べたいもの」で指定してね！", status.id)
      next
    end

    #zero09がつぶやいたらリプライ
~省略~
```

これで毎日の献立に困らない．  

![ご飯1](./img/fifth-2.png)

こんなこともできるので余った食材をうまく使えて経済的．  

![ご飯2](./img/fifth-3.png)


最終系は[こちら](https://github.com/Shandy-ko/raslas_eve)  
"癒し"と"help"を実装．(簡単なので割愛)

これで寂しくない．  

## 参照
 - https://github.com/nzw0301/michil
 - http://qiita.com/nwatanabe/items/7b30de9e7402d3589d00
