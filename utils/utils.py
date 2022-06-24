google_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
            "Chrome/61.0.3163.100 Safari/537.36"

link_key = "link"
hints_key = "hints"

no_metrics_value = "no"

metrics = {
    "yandex": ["//*[contains(@src,'https://mc.yandex.ru/watch')]",
               "//*[contains(text(),'https://mc.yandex.ru/metrika/tag.js')]"],
    "google": ["//script[@src='https://www.google-analytics.com/analytics.js']",
               "//script[contains(text(),'www.google-analytics.com/analytics.js')]",
               "//link[contains(@href,'www.google-analytics.com')]",
               "//script[contains(text(),'www.googletagmanager.com/gtm.js')]",  # google tag manager
               "//script[contains(@src,'www.googletagmanager.com/gtm.js')]",  # google tag manager
               "//script[contains(@src,'www.googletagmanager.com/gtag')]"],  # google tag manager
    "liveinternet": ["//a[@href='https://www.liveinternet.ru/click']",
                     "//script[contains(text(),'counter.yadro.ru/hit')]"]
}
