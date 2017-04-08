项目结构图：

Off_Topic_Detection 

  --KeyWord
      --LDA
          --data
              --testDataSet(待检测作文集输入数据)
              --model_phi.dat(路透社语料库训练好的LDA主题-词分布矩阵)
              --result.txt(LDA提取关键词方法下的输出结果)
              --uptitle.txt(输入的作文题目)
          --Detection_Main1.py(LDA提取关键词的离题检测主程序入口)
          --lda2.py(生成一篇作文的主题-词分布矩阵)
          --pickKeyword.py(提取经过lda2.py处理后的作文关键词)
      --TextRank4ZH
          --example
              --Detection_Main.py(TextRank提取关键词的离题检测主程序入口)
          --test
              --data(待检测作文集输入数据。注意：运行完后输出结果文件result.txt也会放在这里)
              --uptitle.txt(输入的作文题目)

  --Similarity
      --Auto_getThreshold.py(已知各作文为离题或切题的情况下找出最好的阈值，使得F1值最高)
      --F1_Percision_Recall.py(计算F1值、准确率、召回率)
      --getThreshold_ratio.py(获得相关度阈值，以区分离题作文)
      --matplotlib_test.py(数据可视化)
      --Similarity.py(计算待测文本与题目相关度)
      --test.py(遍历文件夹下所有文件名的方法)

  --TitleExpanding
      --word2vec
          --wiki.en.text_50.vector(50维以训练好的词向量数据)
          --WordExpand.py(题目信息扩展方法)