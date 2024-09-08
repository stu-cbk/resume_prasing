package com.example.resume.mapper;

import com.example.resume.entity.SkillInformation;

import java.util.List;

public interface SkillMapper {
    SkillInformation selectByName(String name);
    SkillInformation selectById(Integer id);
    List<SkillInformation> selectAllData();
    Integer addOneData(SkillInformation resume);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
    Integer updateOneData(SkillInformation resume);
}
