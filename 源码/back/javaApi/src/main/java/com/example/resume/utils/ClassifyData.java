package com.example.resume.utils;

import com.example.resume.entity.BasicInformation;
import com.example.resume.entity.EducationalInformation;
import com.example.resume.entity.SkillInformation;
import com.example.resume.entity.WorkInformation;
import com.example.resume.service.BasicService;
import com.example.resume.service.EducationalService;
import com.example.resume.service.WorkService;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.*;
@Data
public class ClassifyData {
    private List<BasicInformation> bList;
    private List<EducationalInformation> eList;
    private List<SkillInformation> sList;
    private List<WorkInformation> wList;
    private Map<String,Object> rMap = new HashMap<>();

    public ClassifyData(List<BasicInformation> b,List<EducationalInformation> e,List<SkillInformation> s,List<WorkInformation> w){
        String s1 = "清华大学、北京大学、厦门大学、中国科学技术大学、南京大学、复旦大学、天津大学、浙江大学、西安交通大学、东南大学、上海交通大学、山东大学、中国人民大学、吉林大学、电子科技大学、四川大学、" +
                "华南理工大学、兰州大学、西北工业大学、同济大学、哈尔滨工业大学、南开大学、华中科技大学、武汉大学、中国海洋大学、湖南大学、北京理工大学、重庆大学、大连理工大学、中山大学、北京航空航天大学、" +
                "东北大学、北京师范大学、中南大学、中国农业大学、国防科技大学、西北农林科技大学、华东师范大学、中央民族大学";
        List<String> s985 = new ArrayList<>(Arrays.asList(s1.split("、")));
        String s2 = "清华大学、北京大学、中国人民大学、北京交通大学、北京工业大学、北京航空航天大学、北京理工大学、北京科技大学、北京化工大学、北京邮电大学、中国农业大学、北京林业大学、" +
                "中国传媒大学、中央民族大学、北京师范大学、中央音乐学院、对外经济贸易大学、北京中医药大学、北京外国语大学、中国地质大学（北京）、中国矿业大学（北京）、中国石油大学（北京）、" +
                "中国政法大学、中央财经大学、华北电力大学、北京体育大学、上海外国语大学、复旦大学、华东师范大学、上海大学、华东大学、上海财经大学、华东理工大学、同济大学、上海交通大学、" +
                "南开大学、天津大学、天津医科大学、河北工业大学、重庆大学、西南大学、太原理工大学、内蒙古大学、大连理工大学、东北大学、辽宁大学、大连海事大学、吉林大学、延边大学、东北师范大学、" +
                "哈尔滨工业大学、哈尔滨工程大学、东北农业大学、东北农林大学、南京大学、东南大学、苏州大学、南京师范大学、中国矿业大学、中国医药大学、河海大学、南京理工大学、江南大学、南京农业大学、" +
                "南京航空航天大学、浙江大学、中国科学技术大学、安徽大学、合肥工业大学、厦门大学、福州大学、南昌大学、山东大学、中国海洋大学、中国石油大学、武汉大学、华中科技大学、武汉理工大学、" +
                "中南财经政法大学、华中师范大学、华中农业大学、中国地质大学、湖南大学、中南大学、湖南师范大学、中山大学、暨南大学、华南理工大学、华南师范大学、广西大学、四川大学、" +
                "西南交通大学、电子科技大学、四川农业大学、西南财经大学、云南大学、贵州大学、西北大学、西安交通大学、西北工业大学、长安大学、西北农林科技大学、陕西师范大学、西安电子科技大学、" +
                "兰州大学、海南大学、西藏大学、新疆大学、石河子大学、第二军医大学、第四军医大学、国防科技大学";
        List<String> s211 = new ArrayList<>(Arrays.asList(s2.split("、")));
        eList = e;
        bList = b;
        wList = w;
        sList = s;
        Map<String,Integer> tmp1 = new HashMap<>();
        Map<String,Integer> tmp2 = new HashMap<>();
        Map<String,Integer> tmp3 = new HashMap<>();
        Map<String,Integer> tmp4 = new HashMap<>();
        tmp1.put("20以下",0);
        tmp1.put("20-30",0);
        tmp1.put("30-40",0);
        tmp1.put("40以上",0);
        tmp2.put("博士",0);
        tmp2.put("硕士",0);
        tmp2.put("本科",0);
        tmp2.put("专科",0);
        tmp2.put("其他",0);
        tmp3.put("985",0);
        tmp3.put("211",0);
        tmp3.put("其他",0);
        tmp4.put("0",0);
        tmp4.put("1-3",0);
        tmp4.put("3-5",0);
        tmp4.put("5以上",0);
        for (int i = 0;i < eList.size();i ++){
            if (bList.get(i).getAge() < 20){
                tmp1.put("20以下",tmp1.get("20以下") + 1);
            }else if(bList.get(i).getAge() < 30){
                tmp1.put("20-30",tmp1.get("20-30") + 1);
            }else if(bList.get(i).getAge() < 40){
                tmp1.put("30-40",tmp1.get("30-40") + 1);
            }else{
                tmp1.put("40以上",tmp1.get("40以上") + 1);
            }

            if (eList.get(i).getEducation().equals("博士")){
                tmp2.put("博士",tmp2.get("博士") + 1);
            }else if (eList.get(i).getEducation().equals("硕士")){
                tmp2.put("硕士",tmp2.get("硕士") + 1);
            }else if (eList.get(i).getEducation().equals("本科")){
                tmp2.put("本科",tmp2.get("本科") + 1);
            }else if (eList.get(i).getEducation().equals("大专") || eList.get(i).getEducation().equals("中专")){
                tmp2.put("专科",tmp2.get("专科") + 1);
            }else {
                tmp2.put("其他",tmp2.get("其他") + 1);
            }

            if (s985.contains(eList.get(i).getUniversity())){
                tmp3.put("985",tmp3.get("985") + 1);
            }else if (s211.contains(eList.get(i).getUniversity())){
                tmp3.put("211",tmp3.get("211") + 1);
            }else {
                tmp3.put("其他",tmp3.get("其他") + 1);
            }

            if (wList.get(i).getWorkExperience() == 0){
                tmp4.put("0",tmp4.get("0") + 1);
            }else if (wList.get(i).getWorkExperience() < 3){
                tmp4.put("1-3",tmp4.get("1-3") + 1);
            }else if (wList.get(i).getWorkExperience() < 5){
                tmp4.put("3-5",tmp4.get("3-5") + 1);
            }else{
                tmp4.put("5以上",tmp4.get("5以上") + 1);
            }
        }
        rMap.put("age",tmp1);
        rMap.put("education",tmp2);
        rMap.put("university",tmp3);
        rMap.put("workExperience",tmp4);
    }
}
