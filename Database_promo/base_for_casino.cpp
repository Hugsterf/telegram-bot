#include <iostream>
#include <cstdint>
#include <string>
#include <fstream>
#include <vector>

bool updateCount(const std::string userpromo, const std::string mainfile, const std::string indexfile);

#pragma pack(push, 1)
struct db
{
    std::string promo;
    int count;
    int payment;

    db() : count(0), promo(""), payment(0) {}

    db(std::string promo, int count, int payment)
    {
        this->promo = promo;
        this->count = count;
        this->payment = payment;
    }
};
#pragma pack(pop)

void savePromo(const db& db, const std::string mainfile, const std::string indexfile)
{
    std::ofstream filemain(mainfile, std::ios::binary | std::ios::app);
    std::ofstream fileindex(indexfile, std::ios::binary | std::ios::app);
    if (!filemain.is_open() or !fileindex.is_open()) {
        std::cout << "Error save filemain";
        exit(0);
    }

    size_t len = db.promo.size();
    fileindex.write(reinterpret_cast<const char*>(&len), sizeof(len));
    filemain.write(db.promo.c_str(), len);
    filemain.write(reinterpret_cast<const char*>(&db.count), sizeof(db.count));
    filemain.write(reinterpret_cast<const char*>(&db.payment), sizeof(db.payment));

    filemain.close();
    fileindex.close();
}

void outPromo(const std::string mainfile, const std::string indexfile)
{
    std::ifstream filemain(mainfile, std::ios::binary);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open())
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    for (uint64_t len : massindex) {
        db user;
        user.promo.resize(len);
        filemain.read(&user.promo[0], len);
        filemain.read(reinterpret_cast<char*>(&user.count), sizeof(user.count));
        filemain.read(reinterpret_cast<char*>(&user.payment), sizeof(user.payment));

        std::cout << "Promo: " << user.promo << std::endl;
        std::cout << "Count: " << user.count << std::endl;
        std::cout << "Payment: " << user.payment << std::endl << std::endl;
    }
}

bool findPromo(const std::string userpromo, const std::string mainfile, const std::string indexfile)
{
    std::ifstream filemain(mainfile, std::ios::binary);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open()) 
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    for (uint64_t len : massindex)
    {
        std::string curpromo;
        curpromo.resize(len);
        filemain.read(&curpromo[0], len);

        filemain.seekg(sizeof(int) * 2, std::ios::cur);

        if (curpromo == userpromo)
        {
            filemain.close();
            fileindex.close();
            if (updateCount(userpromo, mainfile, indexfile) == true)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
    filemain.close();
    fileindex.close();
    return false;
}

bool updateCount(const std::string userpromo, const std::string mainfile, const std::string indexfile)
{
    std::fstream filemain(mainfile, std::ios::binary | std::ios::in | std::ios::out);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open())
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    uint64_t current_pos = 0;
    for (uint64_t len : massindex)
    {
        std::string curpromo;
        curpromo.resize(len);
        filemain.read(&curpromo[0], len);
        int current_count;
        filemain.read(reinterpret_cast<char*>(&current_count), sizeof(current_count));
        filemain.seekg(sizeof(int), std::ios::cur);

        if (curpromo == userpromo)
        {
            if (current_count <= 0)
            {
                filemain.close();
                fileindex.close();
                return false;
            }
            current_count--;
            filemain.seekp(current_pos + len);
            filemain.write(reinterpret_cast<const char*>(&current_count), sizeof(current_count));
            filemain.close();
            fileindex.close();
            return true;
        }
        current_pos += len + sizeof(int);
    }
    filemain.close();
    fileindex.close();
    return false;
}

int find_payment(const std::string promouser, const std::string mainfile, const std::string indexfile)
{
    std::fstream filemain(mainfile, std::ios::binary | std::ios::in | std::ios::out);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open())
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    for (uint64_t len : massindex)
    {
        std::string curpromo;
        int curpay;
        curpromo.resize(len);
        filemain.read(&curpromo[0], len);
        int current_count;
        filemain.read(reinterpret_cast<char*>(&current_count), sizeof(current_count));
        filemain.read(reinterpret_cast<char*>(&curpay), sizeof(curpay));

        if (curpromo == promouser)
        {
            if (current_count <= 0)
            {
                filemain.close();
                fileindex.close();
                return 0;
            }
            return curpay;
            filemain.close();
            fileindex.close();
        }
    }
    filemain.close();
    fileindex.close();
    return 0;
}

extern "C"
{
    __declspec(dllexport) void add_promocode(const char* promocode, int count, int payment);
    __declspec(dllexport) int find_promocode(const char* promocode);
    __declspec(dllexport) int find_payment(const char* promocode);

    void add_promocode(const char* promocode, int count, int payment)
    {
        std::string mainfile = "base.dat";
        std::string indexfile = "index.dat";
        db base(promocode, count, payment);
        savePromo(base, mainfile, indexfile);
    }

    int find_promocode(const char* promocode)
    {
        std::string mainfile = "base.dat";
        std::string indexfile = "index.dat";
        //outPromo(mainfile, indexfile);

        return(findPromo(promocode, mainfile, indexfile)) ? 1 : 0;

        //outPromo(mainfile, indexfile);
    }

    int find_payment(const char* promocode)
    {
        std::string mainfile = "base.dat";
        std::string indexfile = "index.dat";
        return(::find_payment(promocode, mainfile, indexfile));
    }
}