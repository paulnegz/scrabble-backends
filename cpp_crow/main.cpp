#include "string"
#include "crow.h"
#include <set>
#include <chrono>
using namespace std::chrono;

//global variablees
std::set<std::string> WORDS{};
int ELEMENT_COUNT{};

std::set<std::string> get_permutations(std::string letters); 


int main()
{
    crow::SimpleApp app;


    CROW_ROUTE(app, "/ping")([](){
        return "pong";
    });

    //make a redis cache
    //key->name of word, value->figure of speech and 1. definition

    CROW_ROUTE(app, "/scrabble/<string>")([](std::string input){
        auto start = high_resolution_clock::now(); 
	std::string letters = input.substr(0,9);
	crow::json::wvalue res_obj({{}});

        auto permutations = get_permutations(letters);
	//for (const auto& item: permutations){
	//    res_obj[item] = "";
	//}
	
	//nested objects
	crow::json::wvalue es_obj({{"first", "leme"}});
	res_obj["double"] = std::move(es_obj);

	res_obj["length"] = std::to_string(ELEMENT_COUNT);
        auto stop = high_resolution_clock::now(); 
        auto time_duration_ms = duration<double, std::milli>(stop - start); 
        res_obj["time"] = std::to_string(time_duration_ms.count());
	return res_obj;
    });

   /*
    *sample response
    *
    * {
    *   results: [{name: x, fos: y, def: z}, {name: i, fos: j, def: p}]
    *   time: 3.2
    *   length: 50200
    * }
    *
    *
    * */

    app.port(18080).multithreaded().run();

}


void rec_permutation(std::string letters, std::string sub_word){
    ELEMENT_COUNT += 1; 
    for(int i=0; i<letters.length(); i++){
	std::string new_word = sub_word + letters.substr(i,1);
        if (new_word.length() > 2 && true){
           WORDS.insert(new_word);
	}
        rec_permutation(letters.substr(0,i) + letters.substr(i+1), sub_word + letters.substr(i,1));
    }
}

std::set<std::string> get_permutations(std::string letters){ 
    WORDS.clear();
    ELEMENT_COUNT=-1;
    rec_permutation(letters, "");
    std::set<std::string> permutations = WORDS;
    return permutations;
}


