package com.example.resume.service.impl;

import com.example.resume.entity.BasicInformation;
import com.example.resume.mapper.BasicMapper;
import com.example.resume.service.BasicService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class BasicServiceImpl implements BasicService {
    @Resource
    private BasicMapper resumeMapper;

    @Override
    public List<BasicInformation> showAllData(){return resumeMapper.selectAllData();}

    @Override
    public Integer updateOneData(BasicInformation resume){return resumeMapper.updateOneData(resume);}

    @Override
    public Integer insertOneData(BasicInformation resume){return resumeMapper.addOneData(resume);}

    @Override
    public BasicInformation selectByName(String name){return resumeMapper.selectByName(name);}

    @Override
    public BasicInformation selectById(Integer id){return resumeMapper.selectById(id);}

    @Override
    public Integer deleteByName(String name){return resumeMapper.deleteByName(name);}

    @Override
    public Integer deleteById(Integer id){return resumeMapper.deleteById(id);}
}
