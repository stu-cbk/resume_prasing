package com.example.resume.service;

import com.example.resume.entity.SkillInformation;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public interface SkillService {
    List<SkillInformation> showAllData();
    Integer updateOneData(SkillInformation resume);
    Integer insertOneData(SkillInformation resume);
    SkillInformation selectByName(String name);
    SkillInformation selectById(Integer id);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
}

