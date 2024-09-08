package com.example.resume.utils;

import com.example.resume.entity.*;
import lombok.Data;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
@Data
public class ReadExcel {
    private List<Resume> resumeList = new ArrayList<>();
    private List<BasicInformation> basicList = new ArrayList<>();
    private List<EducationalInformation> educationList = new ArrayList<>();
    private List<SkillInformation> skillList = new ArrayList<>();
    private List<WorkInformation> workList = new ArrayList<>();

    public ReadExcel(String filePath){
        try {
            //创建工作簿对象
            XSSFWorkbook xssfWorkbook = new XSSFWorkbook(new FileInputStream(filePath));
            //读取第0个工作表
            XSSFSheet sheet = xssfWorkbook.getSheetAt(0);
            //获取最后一行的num，即总行数。此处从0开始
            int maxRow = sheet.getLastRowNum();
            for (int row = 1; row <= maxRow; row++) {
                //获取最后单元格num，即总单元格数 ***注意：此处从1开始计数***
                Resume resume = getResume(sheet, row);
                BasicInformation basic = getBasic(resume);
                EducationalInformation education = getEducation(resume);
                WorkInformation work = getWork(resume);
                SkillInformation skill = getSkill(resume);
                resumeList.add(resume);
                basicList.add(basic);
                educationList.add(education);
                workList.add(work);
                skillList.add(skill);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static Integer toInteger(String s){
        StringBuilder t = new StringBuilder();
        for (int i = 0;i < s.length();i ++){
            if (s.charAt(i) == '.') break;
            t.append(s.charAt(i));
        }
        return Integer.valueOf(t.toString());
    }

    private BasicInformation getBasic(Resume r){
        BasicInformation b = new BasicInformation();
        b.setId(r.getId());
        b.setName(r.getName());
        b.setAge(r.getAge());
        b.setEmail(r.getEmail());
        b.setIdentity(r.getIdentity());
        b.setOrigin(r.getOrigin());
        b.setPhone(r.getPhone());
        b.setGender(r.getGender());
        return b;
    }

    private EducationalInformation getEducation(Resume r){
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

    private SkillInformation getSkill(Resume r){
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

    private WorkInformation getWork(Resume r){
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

    private Resume getResume(XSSFSheet sheet, int row) {
        Integer id = toInteger(sheet.getRow(row).getCell(0).toString());
        String name = String.valueOf(sheet.getRow(row).getCell(1));
        Integer age = toInteger(sheet.getRow(row).getCell(2).toString());
        String education = String.valueOf(sheet.getRow(row).getCell(3));
        String university = String.valueOf(sheet.getRow(row).getCell(4));
        Integer workExperience = toInteger(sheet.getRow(row).getCell(5).toString());
        String gender = String.valueOf(sheet.getRow(row).getCell(6));
        String targetJob = String.valueOf(sheet.getRow(row).getCell(7));
        String jobs = String.valueOf(sheet.getRow(row).getCell(8));
        String identity = String.valueOf(sheet.getRow(row).getCell(9));
        String origin = String.valueOf(sheet.getRow(row).getCell(10));
        String major = String.valueOf(sheet.getRow(row).getCell(11));
        String companies = String.valueOf(sheet.getRow(row).getCell(12));
        String phone = String.valueOf(sheet.getRow(row).getCell(13));
        String email = String.valueOf(sheet.getRow(row).getCell(14));
        String english = String.valueOf(sheet.getRow(row).getCell(15));
        Integer certNums = toInteger(sheet.getRow(row).getCell(16).toString());
        String schoolTime = String.valueOf(sheet.getRow(row).getCell(17));
        Integer mandarin = toInteger(sheet.getRow(row).getCell(18).toString());
        Integer computer = toInteger(sheet.getRow(row).getCell(19).toString());
        Integer c = toInteger(sheet.getRow(row).getCell(20).toString());
        Integer java = toInteger(sheet.getRow(row).getCell(21).toString());
        Integer python = toInteger(sheet.getRow(row).getCell(22).toString());
        Integer graphicDesign = toInteger(sheet.getRow(row).getCell(23).toString());
        Integer officeSoftware = toInteger(sheet.getRow(row).getCell(24).toString());
        Integer word = toInteger(sheet.getRow(row).getCell(25).toString());
        Integer excel = toInteger(sheet.getRow(row).getCell(26).toString());
        Integer ppt = toInteger(sheet.getRow(row).getCell(27).toString());
        Integer Pr = toInteger(sheet.getRow(row).getCell(28).toString());
        Integer communicate = toInteger(sheet.getRow(row).getCell(29).toString());
        Integer act = toInteger(sheet.getRow(row).getCell(30).toString());
        Integer logic = toInteger(sheet.getRow(row).getCell(31).toString());
        Integer ai = toInteger(sheet.getRow(row).getCell(32).toString());
        String schoolLevel = String.valueOf(sheet.getRow(row).getCell(33));
        Integer engineer = toInteger(sheet.getRow(row).getCell(34).toString());
        Integer finance = toInteger(sheet.getRow(row).getCell(35).toString());
        Integer design = toInteger(sheet.getRow(row).getCell(36).toString());
        Integer manager = toInteger(sheet.getRow(row).getCell(37).toString());
        Integer market = toInteger(sheet.getRow(row).getCell(38).toString());
        Integer hospital = toInteger(sheet.getRow(row).getCell(39).toString());
        Integer edit = toInteger(sheet.getRow(row).getCell(40).toString());
        Integer elseJob = toInteger(sheet.getRow(row).getCell(41).toString());

        Resume resume = new Resume();
        resume.setId(id);
        resume.setAge(age);
        resume.setName(name);
        resume.setEducation(education);
        resume.setUniversity(university);
        resume.setWorkExperience(workExperience);
        resume.setGender(gender);
        resume.setTargetJob(targetJob);
        resume.setJobs(jobs);
        resume.setIdentity(identity);
        resume.setOrigin(origin);
        resume.setMajor(major);
        resume.setCompanies(companies);
        resume.setPhone(phone);
        resume.setEmail(email);
        resume.setEnglish(english);
        resume.setSchoolTime(schoolTime);
        resume.setReward(certNums);
        resume.setMandarin(mandarin);
        resume.setComputer(computer);
        resume.setC(c);
        resume.setJava(java);
        resume.setPython(python);
        resume.setGraphicDesign(graphicDesign);
        resume.setOfficeSoftware(officeSoftware);
        resume.setWord(word);
        resume.setExcel(excel);
        resume.setPpt(ppt);
        resume.setPr(Pr);
        resume.setCommunicate(communicate);
        resume.setAct(act);
        resume.setLogic(logic);
        resume.setAi(ai);
        resume.setSchoolLevel(schoolLevel);
        resume.setEngineer(engineer);
        resume.setFinance(finance);
        resume.setDesign(design);
        resume.setManager(manager);
        resume.setMarket(market);
        resume.setHospital(hospital);
        resume.setEdit(edit);
        resume.setElseJob(elseJob);
        return resume;
    }
}
