/*
Project:COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities_Analytics on the Cloud
Team:group05--Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia Yin (1017231), Fang Qu (1070888)
*/


var auth = btoa('admin:admin');

    var char5 = [];
            $.ajax({
        url:'http://172.26.134.56:5984/view_results(australia_tweets)/australia_alcohol_hashtag_count',
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
        char5 = data.rows;
     //  console.log( pageTotal)
        },
        error:function(data){
            console.log('request failed')
        }
    });

var char5Data1 = [];
var char5Data2 = [];



for (i=0; i<char5.length; i++) {
    char5Data1.push(char5[i].key.toLowerCase());
    char5Data2.push({'name':char5[i].key.toLowerCase(),'value':char5[i].value});


}

   //    console.log(Data1);
// console.log(Data2);












     var ectest = echarts.init(document.getElementById("charts5"));
    option = {
    title: {
        text: 'All alcohol hashtags in Australia',
        subtext: 'Top 20',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    // legend: {
    //     type: 'scroll',
    //     orient: 'vertical',
    //     right: 10,
    //     top: 20,
    //     bottom: 20,
    //     data: char5Data1,
    //
    //     //selected: data.selected
    // },
    series: [
        {
            name: 'hashtag',
            type: 'pie',
            radius: '40%',
            center: ['50%', '50%'],
            data:  char5Data2,
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
