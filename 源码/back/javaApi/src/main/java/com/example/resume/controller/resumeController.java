package com.example.resume.controller;

import com.example.resume.entity.*;
import com.example.resume.service.BasicService;
import com.example.resume.service.EducationalService;
import com.example.resume.service.SkillService;
import com.example.resume.service.WorkService;
import com.example.resume.utils.ClassifyData;
import com.example.resume.utils.ClassifyResume;
import com.example.resume.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/resume")
//@CrossOrigin(origins = "http://localhost:8080")
@CrossOrigin
public class resumeController {
    @Autowired
    BasicService basicService;
    @Autowired
    EducationalService educationalService;
    @Autowired
    WorkService workService;
    @Autowired
    SkillService skillService;

    @GetMapping("/showBasicData")
    public Result showBasicData(){
        List<BasicInformation> bList = basicService.showAllData();
        return Result.suc(bList);
    }

    @GetMapping("/selectBasicByName")
    public Result selectBasicByName(@RequestParam("name")  String name){
        BasicInformation basicInformation = basicService.selectByName(name);
        if (basicInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(basicInformation);
        }
    }

    @GetMapping("/selectBasicById")
    public Result selectBasicById(@RequestParam("id") Integer id){
        BasicInformation basicInformation = basicService.selectById(id);
        if (basicInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(basicInformation);
        }
    }

    @GetMapping("/showEducationalData")
    public Result showEducationalData(){
        List<EducationalInformation> eList = educationalService.showAllData();
        return Result.suc(eList);
    }

    @GetMapping("/selectEducationalByName")
    public Result selectEducationalByName(@RequestParam("name") String name){
        EducationalInformation educationalInformation = educationalService.selectByName(name);
        if (educationalInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(educationalInformation);
        }
    }

    @GetMapping("/selectEducationalById")
    public Result selectEducationalById(@RequestParam("id") Integer id){
        EducationalInformation educationalInformation = educationalService.selectById(id);
        if (educationalInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(educationalInformation);
        }
    }

    @GetMapping("/showWorkData")
    public Result showWorkData(){
        List<WorkInformation> wList = workService.showAllData();
        return Result.suc(wList);
    }

    @GetMapping("/selectWorkByName")
    public Result selectWorkByName(@RequestParam("name") String name){
        WorkInformation workInformation = workService.selectByName(name);
        if (workInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(workInformation);
        }
    }

    @GetMapping("/selectWorkById")
    public Result selectWorkById(@RequestParam("id") Integer id){
        WorkInformation workInformation = workService.selectById(id);
        if (workInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(workInformation);
        }
    }

    @GetMapping("/showSkillData")
    public Result showSkillData(){
        List<SkillInformation> sList = skillService.showAllData();
        return Result.suc(sList);
    }

    @GetMapping("/selectSkillByName")
    public Result selectSkillByName(@RequestParam("name") String name){
        SkillInformation skillInformation = skillService.selectByName(name);
        if (skillInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(skillInformation);
        }
    }

    @GetMapping("/selectSkillById")
    public Result selectSkillById(@RequestParam("id") Integer id){
        SkillInformation skillInformation = skillService.selectById(id);
        if (skillInformation == null){
            return Result.fail("查询失败");
        }else{
            return Result.suc(skillInformation);
        }
    }

    @GetMapping("/classifyData")
    public Result classifyData(){
        List<BasicInformation> b = basicService.showAllData();
        List<EducationalInformation> e = educationalService.showAllData();
        List<SkillInformation> s = skillService.showAllData();
        List<WorkInformation> w = workService.showAllData();
        ClassifyData c = new ClassifyData(b,e,s,w);
        if (c.getRMap().size() > 0){
            return Result.suc(c.getRMap());
        }else{
            return Result.fail("分类失败");
        }
    }

    @PostMapping("/classifyResume")
    public Result classifyResume(@RequestBody Resume r){
        //System.out.print(r);
        BasicInformation b1 = basicService.selectByName(r.getName());
        if (b1 == null){
            Integer x1 = basicService.insertOneData(ClassifyResume.getBasic(r));
            BasicInformation b2 = basicService.selectByName(r.getName());
            r.setId(b2.getId());
            Integer x2 = educationalService.insertOneData(ClassifyResume.getEducation(r));
            Integer x4 = skillService.insertOneData(ClassifyResume.getSkill(r));
            Integer x3 = workService.insertOneData(ClassifyResume.getWork(r));
            if (x1 + x2 + x3 + x4 != 4){
                return Result.fail("插入失败");
            }
        }else{
            r.setId(b1.getId());
            Integer x1 = basicService.updateOneData(ClassifyResume.getBasic(r));
            Integer x2 = educationalService.updateOneData(ClassifyResume.getEducation(r));
            Integer x3 = workService.updateOneData(ClassifyResume.getWork(r));
            Integer x4 = skillService.updateOneData(ClassifyResume.getSkill(r));
            if (x1 + x2 + x3 + x4 != 4){
                return Result.fail("更改失败");
            }
        }
        BasicInformation b2 = basicService.selectByName(r.getName());
        return Result.suc(b2.getId());
    }

    @PostMapping("/classifyMultiResume")
    public Result classifyMultiResume(@RequestBody List<Resume> rList){
        List<Integer> iList = new ArrayList<>();
        for (Resume r:rList){
            BasicInformation b1 = basicService.selectByName(r.getName());
            if (b1 == null){
                Integer x1 = basicService.insertOneData(ClassifyResume.getBasic(r));
                BasicInformation b2 = basicService.selectByName(r.getName());
                r.setId(b2.getId());
                Integer x2 = educationalService.insertOneData(ClassifyResume.getEducation(r));
                Integer x4 = skillService.insertOneData(ClassifyResume.getSkill(r));
                Integer x3 = workService.insertOneData(ClassifyResume.getWork(r));
                if (x1 + x2 + x3 + x4 != 4){
                    return Result.fail("插入失败");
                }
            }else{
                r.setId(b1.getId());
                Integer x1 = basicService.updateOneData(ClassifyResume.getBasic(r));
                Integer x2 = educationalService.updateOneData(ClassifyResume.getEducation(r));
                Integer x3 = workService.updateOneData(ClassifyResume.getWork(r));
                Integer x4 = skillService.updateOneData(ClassifyResume.getSkill(r));
                if (x1 + x2 + x3 + x4 != 4){
                    return Result.fail("更改失败");
                }
            }
            BasicInformation b2 = basicService.selectByName(r.getName());
            iList.add(b2.getId());
        }
        return Result.suc(iList);
    }

    @PostMapping("/lightResume")
    public Result lightResume(@RequestBody Resume r){
        List<String> sList = new ArrayList<>();
        if (r.getSchoolLevel().equals("985") || r.getSchoolLevel().equals("211")){
            String s1 = "院校背景不错,毕业于" + r.getSchoolLevel() + "大学，学历为" + r.getEducation();
            sList.add(s1);
        }
        if (r.getEnglish().equals("六级")){
            String s2 = "英语背景良好,可以流利地进行听说读写";
            sList.add(s2);
        }
        if (r.getComputer() >= 5 || r.getOfficeSoftware() >= 4){
            String s3 = "计算机背景不错，可以熟练使用办公软件";
            sList.add(s3);
        }
        if (r.getReward() >= 4){
            String s4 = "综合能力强，获取证书数量多";
            sList.add(s4);
        }
        if (r.getCommunicate() == 1){
            String s5 = "性格开朗大方，有良好的社会交往能力";
            sList.add(s5);
        }
        if (r.getLogic() == 1){
            String s6 = "逻辑分析能力强,对数据较敏感";
            sList.add(s6);
        }
        if (r.getAi() == 1){
            String s7 = "熟练使用ai工具,可以结合人工智能解决问题";
            sList.add(s7);
        }
        if (r.getAct() == 1){
            String s8 = "行动力强,有责任心";
            sList.add(s8);
        }
        return Result.suc(sList);
    }

}
