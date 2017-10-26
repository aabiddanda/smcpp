#ifndef HMM_H
#define HMM_H

#include <map>

class InferenceManager;
struct InferenceBundle;

class HMM
{
    friend class InferenceManager;

    public:
    HMM(const int hmm_num,
        const Eigen::Map<Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > &obs,
        const InferenceBundle *ib);
    void Estep(bool);
    double loglik(void);
    Vector<adouble> Q(void);

    private:
    HMM(HMM const&) = delete;
    HMM& operator=(HMM const&) = delete;
    // Methods
    void domain_error(double);
    inline block_key ob_key(int i) { return block_key(obs.row(i).transpose().tail(obs.cols() - 1)); }

    // Instance variables
    const int hmm_num;
    const Eigen::Map<Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > obs;
    const InferenceBundle *ib;
    const int M, L;
    double ll;
    Matrix<double> alpha_hat, xisum, gamma;
    Vector<double> c;
    std::map<block_key, Vector<double> > gamma_sums;
};

#endif
