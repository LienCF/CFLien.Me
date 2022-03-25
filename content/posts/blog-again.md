+++
draft = false
date = 2021-07-18T15:24:34+08:00
title = "再出發"
description = ""
slug = ""
authors = []
tags = ["blog", "hugo", "netlify", "github", "google analytics", "google search console"]
categories = ["blog", "hugo"]
externalLink = ""
series = []
+++

上次寫部落格已經是 N 年前的事了，決定再出發是因為現在記性越來越差了，想留個空間記錄一下最近在看的東西及生活的點滴。

首先就從這個新的 Blog 相關的東西開始吧。

建立這個 Blog ，用到了以下的服務與技術，之後會再針對每個選擇做介紹

* 網址：[CFLien.Me](https://cflien.me)
  
  網址是從 [alldomains.hosting(推廣連結)](https://manage.alldomains.hosting/subject_index.php?rsaction=submit_come&amp;i=7733400&amp;r=https%3A%2F%2Falldomains.hosting%2Fen%2Fregister-domain.html) 申請的，原因是因為它便宜，搜尋界面也還行。但等過段時間後，會考慮把 domain 轉到 [google](https://domains.google) 或是 [cloudflare](https://www.cloudflare.com/zh-tw/products/registrar/)。

* DNS 管理：[cloudflare](https://www.cloudflare.com)
  
  申請完網址後，可以在 alldomains 的後台管理 DNS，但我一開始是打算使用 cloudflare 的 CDN 的，所以就直接把 DNS 給改到 cloudflare 去管理了。

* Blog 方案：[Hugo](https://gohugo.io)
  
  考慮了幾個平台，有 [Medium](https://medium.com), [WordPress](https://wordpress.com/zh-tw/), 及靜態網頁產生的工具如 [Hugo](https://gohugo.io) 等的。最後考慮了需求及因為想玩玩不一樣的東西，最終選擇了 Hugo 為這次的平台。(但說不定過陣子就又改變主意了)

* Hosting：[netlify](https://www.netlify.com)
  
  找到解決方案後，再來考慮的就是要把網頁 Host 在什麼地方。考慮過 oracle cloud, firebase, github page, netlify, [Vercel](https://vercel.com) 等的方案。最後是選擇了 netlify 。因為有不錯的 CI/CD 整合，再加上台灣的連線速度相當不錯，還有免費的 serverless 也許未來也可以玩玩看。就暫時選擇它了。

* Hugo 主題：[Hugo-Coder](https://github.com/luizdepra/hugo-coder)
  
  這也是個對於有選擇困難的人的痛。身為一個選擇困難者，每個主題看起來都很棒。最後是先選用 hugo-coder 主題來用用看。[ananke](https://github.com/theNewDynamic/gohugo-theme-ananke.git) 及 [Mainroad](https://github.com/Vimux/Mainroad/) 做為備選。(用 Markdown 寫作的好處就是內容與呈現是分離的，所以換主題很方便)

* 網站分析與 SEO：[Google Analytics](https://analytics.google.com/analytics/web) 及 [Google Search Console](https://search.google.com/search-console)
  
  用來分析流量及搜尋引擎最佳化用的。寫了東西當然還是希望會有人看，能對除了我自己以外的人也能有些幫助。Hugo 對於 Google Analytics 及 sitemap 都有相當不錯的支援，整合上相當的方便。當然要做好 SEO (Search Engine Optimization) 還是有很多技巧，好可以趁這個機會也學學。

* 寫作工具：[Obsidian](https://obsidian.md), [Typora](https://www.typora.io), [VSCode](https://code.visualstudio.com)
  
  比較了一些工具，像是 MacDown, Ulysses, Craft, Obsidian, Typora 等等，雖然是 Markdown 的寫作工具，但功能上還是有一些小小的差異。最後考量方便性、格式、預覽等的功能上，先選擇了 Typora 及 Obsidian 做為寫作工具。
