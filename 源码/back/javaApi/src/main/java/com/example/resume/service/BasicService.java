package com.example.resume.service;

import com.example.resume.entity.BasicInformation;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface BasicService {
    List<BasicInformation> showAllData();
    Integer updateOneData(BasicInformation resume);
    Integer insertOneData(BasicInformation resume);
    BasicInformation selectByName(String name);
    BasicInformation selectById(Integer id);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
}
