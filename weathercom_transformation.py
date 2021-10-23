import pandas as pd
import datetime

df = pd.read_csv("dataset_weathercom1_2021-10-23_09-07-04-902.csv", encoding="utf-8")

#url = "https://weather.com/weather/tenday/l/" + locationID
locationIDs = {
    "Cheb" : "61abc6b803796e59d6b735e0a8394abcbaa25575a360d0ab8b0e772a38b845f7",
    "Karlovy Vary" : "c156caec7a5e871553e6769e82bb24a5e9d23172b2a8e387124ca61e64f71b4b", 
    "Přimda": "f7a8a558d6a2964fdcd45429435a0b953f21d84559fefb969335aa66265a5798", 
    "Kopisty": "d2a6ea51a93e14100014765b4ce83dd96f37114b377d68835c1c2bb7ee34f6f6", 
    "Tušimice": "b1c1a8721569b42db6c7c7deaf17e8e0394cdc1e63e39d62757458488f520879", 
    "Plzeň-Mikulka": "01a02856a1fde3883726785adbcf5a99a0a3396f6f457d8230904c446306f279", 
    "Churáňov": "56f788bf3e3c1522d75d51a2edc42db42eed1bc49f3540ec1c731f1505ba0245", 
    "Milešovka": "8d406a8b3223659d4b8a98b2f82bafac4b7c1acff1deef9cb6ff4808c37a5604", 
    "Kocelovice": "695bdead27bdd4249476d7c0a0fb5f226276df6aff55c3e7794b543076a50614", 
    "Ústí nad Labem" : "141d47e5fece55949584a012ad4f7e6f46f41893ad76985e1a627c94dfefa48a",
    "Doksany": "c2c0d0601e0907589dba2055866f0ba8943c019255b7458001f969ce34058fe9", 
    "Praha-Ruzyně": "855ebbe69a4ce081ee4b27b05ccdbd97cc202b3e12239134ab2ac6d5ae92400b",
    "Praha-Karlov": "81cbe8a06fd80171651aef7a414bce1e599aa05082d82f4e319f94b4b60602e0", 
    "Praha-Libuš": "b50464f6ca71e0221cdde1754f9238cf863f83645c7e1cc1f7e5d1f42f7b6bc4", 
    "Temelín": "5fc341840c16c080b0c297f145eadc7ac439c50ac4704a9da986b701b9cf133d", 
    "České Budějovice": "b6dc300cea6e6b4c36035bb679849694e883f8bc225de1bc9e1dae691f6d3e96", 
    "Praha-Kbely": "#", 
    "Liberec": "0f982af7a29a083094eccfe65c7d3cab34047ecea958f0fe7c970d6e15f210ff", 
    "Jičín": "8d40e4e1b4384ca7e6de1bf9df5054a4bb7f55a21c8994d7284c4dd1ac8a5623", 
    "Čáslav": "67ad0b2dc3d32da0397076281bf5c15cfae5de8918f7c3a58dedf36266c49ec2", 
    "Košetice": "9e763540ad6b5ac58e94b741d77f0c2b344d539b96b603b71f38a19db433624a", 
    "Kostelní Myslová": "f1eae844e3f5f95e6784a5a708f4af6258fe225fefad33bd597038a10539c805", 
    "Pec pod Sněžkou": "036606dfc47801b11108040000b0fff34bb046232b0a4a620b955ff360a493bb", 
    "Pardubice": "e34b9adc73298661d13487286f4b29e72e5202b61132e0d0832311818d5c4c75", 
    "Přibyslav": "1bde95b07b0cb7dc74bc8cff314d409b503a0790dfd718a0e1c62d7a798f420b", 
    "Polom": "c1a96f29c9edbbff27c366594a717fda985470680e4e38137f315cb11359f42c", 
    "Ústí nad Orlicí": "d5ae3d2f225a4e22e551afe8b58762f2728269fb4e2a2b4bf831f7cd077166af", 
    "Svratouch": "3e9cd0b2163f9bbe346ccc22176a11ac26ccd4723a9d9384327bcdc40430430a", 
    "Náměšť nad Oslavou": "c92d7704e8d9e93094de8ba037ca3810a1a787f5ca5341ac8e86c0ec03482be7", 
    "Dukovany": "6616f6d0c1da990cc5ef12eca89145efdaa40ab941dd501de00b47295d6a365a", 
    "Kuchařovice": "5a093ec63fb7de458e4e319cb3e1dadc536f3b5f2fc695163d8bde315aae8f85", 
    "Luká": "b9add27942db714cc2f27c1955ebbce724dd20f700a821bc72c4ffb069a8aada", 
    "Brno-Tuřany": "b9791d105b0af07705b1e9a61e313ae785fb1fe912dec7d6a607821d299de7e1", 
    "Šerák": "46569898b236e955e20c2cc4546f823c6d97a6133c1839d36cd9ab2f4e15b2d4", 
    "Prostějov": "b6d6f4ffa32180e47282dcae2723b60ea02bdd07c8819279ec5b32e0fac75a60", 
    "Červená u Libavé": "a3db382cbc6de197c4f7bd43a07ee6da447d9a35d4f1e0e6723c0e9aa48dbc36", 
    "Holešov": "67a94d5b9e1cdc7dca56e3088867367da1d00eef0dedfb9a5aeda39f0ef7d948", 
    "Ostrava-Mošnov": "38167146c1f54521a434315934d7a970d4652bfc4d86ac2d6739aa0c752c075d", 
    "Lysá hora": "20e28455a2d19334c93f946dc702bbfc982b1aea146ec4bf27269148abfca46d", 
    "Maruška": "cf9533286d3c14eb7cd642aa43b0e56aeae3b0877f0bba48f6809cb627f8a800", 
}

d={"location_name":locationIDs.keys(), 
"locationId":locationIDs.values(), }

locationsdf = pd.DataFrame.from_dict(d, orient="columns")
joindf = pd.merge(df, locationsdf, on="locationId")

joindf["date_stamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:00:00")

joindf.to_csv("weathercom_tab.csv", index=False)
