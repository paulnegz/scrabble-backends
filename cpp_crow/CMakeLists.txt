cmake_minimum_required(VERSION 3.5)

project (word_game)

set(INCLUDE_PATHS boost_1_83_0 Crow-1.0-5/include)

#set(INCLUDE_PATHS boost_1_83_0 crow/include)

add_executable(word_game main.cpp)

target_include_directories(word_game PUBLIC $(INCLUDE_PATHS))
