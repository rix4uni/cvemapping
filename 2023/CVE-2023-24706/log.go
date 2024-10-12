package main

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"os"
)

var Logger = InitLogger()

func InitLogger() *zap.Logger {

	//获取编码器
	encoderConfig := zap.NewProductionEncoderConfig() //NewJSONEncoder()输出json格式，NewConsoleEncoder()输出普通文本格式
	//encoderConfig := zap.NewDevelopmentEncoderConfig()                                //NewJSONEncoder()输出json格式，NewConsoleEncoder()输出普通文本格式
	encoderConfig.EncodeTime = zapcore.TimeEncoderOfLayout("2006-01-02 15:04:05.000") //指定时间格式
	encoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder                      //按级别显示不同颜色，不需要的话取值zapcore.CapitalLevelEncoder就可以了
	//encoderConfig.EncodeCaller = zapcore.FullCallerEncoder //显示完整文件路径
	encoder := zapcore.NewConsoleEncoder(encoderConfig)

	////文件writeSyncer
	//fileWriteSyncer := zapcore.AddSync(&lumberjack.Logger{
	//	Filename:   "./info.log", //日志文件存放目录
	//	MaxSize:    10,           //文件大小限制,单位MB
	//	MaxBackups: 5,            //最大保留日志文件数量
	//	MaxAge:     30,           //日志文件保留天数
	//	Compress:   false,        //是否压缩处理
	//})
	//第三个及之后的参数为写入文件的日志级别,ErrorLevel模式只记录error级别的日志
	fileCore := zapcore.NewCore(encoder, zapcore.NewMultiWriteSyncer(zapcore.AddSync(os.Stdout)), zapcore.DebugLevel)

	return zap.New(fileCore, zap.AddCaller()) //AddCaller()为显示文件名和行号
}
