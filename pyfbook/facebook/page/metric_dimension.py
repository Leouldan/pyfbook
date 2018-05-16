metric_dimension = {
    "page_all_days": {
        "metric": [
            "page_impressions",
            "page_impressions_unique",
            "page_impressions_paid",
            "page_impressions_paid_unique",
            "page_impressions_organic",
            "page_impressions_organic_unique",
            "page_engaged_users",
            "page_post_engagements",
            "page_fan_adds_unique",
            "page_posts_impressions",
            "page_posts_impressions_unique",
            "page_posts_impressions_paid",
            "page_posts_impressions_paid_unique",
            "page_posts_impressions_organic",
            "page_posts_impressions_organic_unique"
        ],
        "period": [
            "day",
            ],
        "date_window": "lifetime",
        "dimension": [
            "page_id",
            "end_time",
            "period"
        ]
    },

    "page_fan": {
        "metric": [
            "page_fans"
        ],
        "period": [
            "lifetime"
            ],
        "date_window": "lifetime",
        "dimension": [
            "page_id",
            "end_time",
            "period"
        ]
    },

    "page_fan_add": {
        "metric": [
            "page_fan_adds",
            "page_fan_removes"
        ],
        "period": [
            "day"
        ],
        "date_window": {
            "since": "2017-01-01",
            "until": "2018-01-15"
        },
        "dimension": [
            "page_id",
            "end_time",
            "period",
        ]
    }
}
