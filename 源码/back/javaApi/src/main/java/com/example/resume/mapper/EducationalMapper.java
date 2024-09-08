package com.example.resume.mapper;

import com.example.resume.entity.EducationalInformation;

import java.util.List;

public interface EducationalMapper {
    EducationalInformation selectByName(String name);
    EducationalInformation selectById(Integer id);
    List<EducationalInformation> selectAllData();
    Integer addOneData(EducationalInformation resume);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
    Integer updateOneData(EducationalInformation resume);
}
