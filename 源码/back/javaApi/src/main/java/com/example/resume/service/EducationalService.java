package com.example.resume.service;

import com.example.resume.entity.EducationalInformation;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface EducationalService {
    List<EducationalInformation> showAllData();
    Integer updateOneData(EducationalInformation resume);
    Integer insertOneData(EducationalInformation resume);
    EducationalInformation selectByName(String name);
    EducationalInformation selectById(Integer id);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
}
