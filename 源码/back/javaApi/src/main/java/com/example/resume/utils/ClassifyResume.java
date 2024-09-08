package com.example.resume.utils;

import com.example.resume.entity.*;

public class ClassifyResume {
    public static BasicInformation getBasic(Resume r){
        BasicInformation b = new BasicInformation();
        b.setId(r.getId());
        b.setName(r.getName());
        b.setAge(r.getAge());
        b.setEmail(r.getEmail());
        b.setIdentity(r.getIdentity());
        b.setOrigin(r.getOrigin());
        b.setPhone(r.getPhone());
        b.setGender(r.getGender());
        b.setText(r.getText());
        return b;
    }

    public static EducationalInformation getEducation(Resume r){
        EducationalInformation e = new EducationalInformation();
        e.setId(r.getId());
        e.setEducation(r.getEducation());
        e.setMajor(r.getMajor());
        e.setName(r.getName());
        e.setUniversity(r.getUniversity());
        e.setSchoolTime(r.getSchoolTime());
        e.setSchoolLevel(r.getSchoolLevel());
        return e;
    }

    public static SkillInformation getSkill(Resume r){
        SkillInformation s = new SkillInformation();
        s.setId(r.getId());
        s.setName(r.getName());
        s.setMandarin(r.getMandarin());
        s.setEnglish(r.getEnglish());
        s.setComputer(r.getComputer());
        s.setC(r.getC());
        s.setJava(r.getJava());
        s.setPython(r.getPython());
        s.setGraphicDesign(r.getGraphicDesign());
        s.setOfficeSoftware(r.getOfficeSoftware());
        s.setWord(r.getWord());
        s.setPpt(r.getPpt());
        s.setExcel(r.getExcel());
        s.setPr(r.getPr());
        s.setCommunicate(r.getCommunicate());
        s.setLogic(r.getLogic());
        s.setAct(r.getAct());
        s.setAi(r.getAi());
        s.setReward(r.getReward());
        return s;
    }

    public static WorkInformation getWork(Resume r){
        WorkInformation w = new WorkInformation();
        w.setId(r.getId());
        w.setName(r.getName());
        w.setJobs(r.getJobs());
        w.setWorkExperience(r.getWorkExperience());
        w.setTargetJob(r.getTargetJob());
        w.setCompanies(r.getCompanies());
        w.setEngineer(r.getEngineer());
        w.setDesign(r.getDesign());
        w.setEdit(r.getEdit());
        w.setFinance(r.getFinance());
        w.setHospital(r.getHospital());
        w.setElseJob(r.getElseJob());
        w.setManager(r.getManager());
        w.setMarket(r.getMarket());
        return w;
    }
}
