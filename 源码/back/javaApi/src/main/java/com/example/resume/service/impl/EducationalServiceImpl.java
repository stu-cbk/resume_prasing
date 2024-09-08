package com.example.resume.service.impl;

import com.example.resume.entity.EducationalInformation;
import com.example.resume.mapper.EducationalMapper;
import com.example.resume.service.EducationalService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class EducationalServiceImpl implements EducationalService {
    @Resource
    private EducationalMapper resumeMapper;

    @Override
    public List<EducationalInformation> showAllData(){return resumeMapper.selectAllData();}

    @Override
    public Integer updateOneData(EducationalInformation resume){return resumeMapper.updateOneData(resume);}

    @Override
    public Integer insertOneData(EducationalInformation resume){return resumeMapper.addOneData(resume);}

    @Override
    public EducationalInformation selectByName(String name){return resumeMapper.selectByName(name);}

    @Override
    public EducationalInformation selectById(Integer id){return resumeMapper.selectById(id);}

    @Override
    public Integer deleteByName(String name){return resumeMapper.deleteByName(name);}

    @Override
    public Integer deleteById(Integer id){return resumeMapper.deleteById(id);}

}
