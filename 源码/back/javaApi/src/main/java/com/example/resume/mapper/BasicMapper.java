package com.example.resume.mapper;

import com.example.resume.entity.BasicInformation;

import java.util.List;

public interface BasicMapper {
    BasicInformation selectByName(String name);
    BasicInformation selectById(Integer id);
    List<BasicInformation> selectAllData();
    Integer addOneData(BasicInformation resume);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
    Integer updateOneData(BasicInformation resume);
}
