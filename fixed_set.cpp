#include <iostream>
#include <vector>
#include <fstream>
#include <random>
#include <limits>
#include <memory>

class Random {
public:
    Random() {}

    int64_t GetRandom() {
        return distribution(mt);
    }

private:
    std::uniform_int_distribution<int64_t> distribution;
    std::mt19937 mt;
};


class BaseSet {
public:
    BaseSet() {}

    void RerandomCoeffs() {
        a_number_ = random_.GetRandom() % (P_num - 1) + 1;
        b_number_ = random_.GetRandom() %  P_num;
    }

    int64_t GetHash(int64_t number) {
        return (((a_number_ * number + b_number_) % P_num) % (size_));
    }

protected:
    static const int64_t  P_num = 2971215073;
    int64_t a_number_, b_number_;
    u_int64_t size_ = 0;
    static Random random_;
    const int64_t INF = 1000000007;
};


Random BaseSet::random_;


class Bucket: BaseSet{
public:
    Bucket() {
        RerandomCoeffs();
        size_ = 0;
    }

    const std::vector<int64_t>& GetKeys() {
        return keys_;
    }

    void AddKey(int64_t value) {
        keys_.push_back(value);
    }

    void ClearKeys() {
        keys_.clear();
    }

    int64_t GetKeysSize() {
        return keys_.size();
    }

    void Initialize() {
        ResizeHashedKeys();
        RerandomCoeffs();
        int64_t cur_hash;
        auto key_iterator = GetKeys().begin();
        while (key_iterator != GetKeys().end()) {
            cur_hash = GetHash(*key_iterator);
            if (hashed_keys_[cur_hash] == INF) {
                hashed_keys_[cur_hash] = *key_iterator;
            } else {
                RerandomCoeffs();
                for (int64_t& lol : hashed_keys_) {
                    lol = INF;
                }
                key_iterator = GetKeys().begin() - 1;
            }
            ++key_iterator;
        }
    }

    bool Contains(int64_t number) {
        if (0 == size_)
            return false;
        int64_t hash = GetHash(number);
            return hashed_keys_[hash] == number;
    }

 private:
    void ResizeHashedKeys() {
        size_ = GetKeysSize() * GetKeysSize();
        hashed_keys_.resize(size_, INF);
    }

    std::vector<int64_t> keys_;
    std::vector<int64_t> hashed_keys_;
};


class FixedSet: BaseSet{
 public:
    FixedSet() {}

    void Initialize(const std::vector<int64_t> &numbers) {
        size_ = numbers.size();
        buckets_.resize(size_);
        RerandomCoeffs();
        int64_t quadratic_sum = 0;
        int64_t max_sum = max_sum_coefficent_ * size_;
        do {
            RerandomCoeffs();
            for (int64_t number : numbers) {
                buckets_[GetHash(number)].AddKey(number);
            }
            quadratic_sum = 0;

            for (Bucket& bucket : buckets_) {
                quadratic_sum += bucket.GetKeysSize() * bucket.GetKeysSize();
            }

            if (quadratic_sum > max_sum) {
                for (Bucket& bucket : buckets_) {
                    bucket.ClearKeys();
                }
            }
        }  while (quadratic_sum > max_sum);

        for (Bucket& bucket : buckets_) {
            bucket.Initialize();
        }
    }

    bool Contains(int64_t number) {
        return buckets_[GetHash(number)].Contains(number);
    }

private:
    static const int64_t max_sum_coefficent_ {4};
    std::vector<Bucket> buckets_;
};

int64_t GetNumberWithOffset(int64_t number) {
    return number + 1073741823;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    srand(time(nullptr));

    int64_t numbers_len;
    std::cin >> numbers_len;
    std::vector<int64_t> numbers(numbers_len);
    for (int64_t& number : numbers) {
        std::cin >> number;
        number = GetNumberWithOffset(number);
    }

    FixedSet fixedSet;
    fixedSet.Initialize(numbers);
    int64_t queries_number;
    std::cin >> queries_number;

    for (int64_t j = 0; j < queries_number; ++j) {
        int64_t query;
        std::cin >> query;
        std::cout << (fixedSet.Contains(GetNumberWithOffset(query)) ? "Yes\n" : "No\n");
    }
}
