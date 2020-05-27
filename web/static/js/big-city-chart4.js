/*
Project:COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities_Analytics on the Cloud
Team:group05--Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia Yin (1017231), Fang Qu (1070888)
*/

var auth = btoa('admin:admin');

    var char4 = [];
            $.ajax({
        url:'http://172.26.134.56:5984/view_results(australia_tweets)/australia_hashtag_count',
        dataType:'json',
       async : false,
                xhrFields:{
      withCredentials:true
            },
       headers: {
        "Authorization": "Basic " + auth
    },
            crossDomain:true,

        success:function(data){
        char4 = data.rows;
     //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });

var char4Data1 = [];
var char4Data2 = [];



for (i=0; i<char4.length; i++) {
    char4Data1.push(char4[i].key.toLowerCase());
    char4Data2.push({'name':char4[i].key.toLowerCase(),'value':char4[i].value});


}

// console.log(Data1);
// console.log(Data2);

var ectest = echarts.init(document.getElementById("charts4"));
    option = {
    title: {
        text: 'All topic hashtags in Australia',
        subtext: 'Top 20',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    series: [
        {
            name: 'hashtag',
            type: 'pie',
            radius: '45%',
            center: ['50%', '50%'],
            data:  char4Data2,
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
 ectest.setOption(option);
