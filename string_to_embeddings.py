import numpy as np
from cbow_from_json import apply_cleaning_to_string

EMBEDDING_LOOKUP_FILENAME = 'embedding_lookup.npy'
UNKNOWN_TOKEN = 'UNK'


def load_lookup():
    """Loads embedding lookup file. For ease of use, returns a Python dictionary"""
    py_dict = {}
    np_lookup = np.load(EMBEDDING_LOOKUP_FILENAME)
    for key in np_lookup.item().keys():
        py_dict[key] = np_lookup.item().get(key)
    return py_dict


def create_vector_set_from_string(input_string, vector_lookup=None):
    """Return 2d numpy array of word embeddings for a string"""

    if vector_lookup is None:
        vector_lookup = load_lookup()

    cleaned = apply_cleaning_to_string(input_string)
    vector_list = []
    for word in cleaned.split(' '):
        try:
            vector_list.append(vector_lookup[word])
        except KeyError:
            vector_list.append(vector_lookup[UNKNOWN_TOKEN])
    return np.array(vector_list)


def main():
    from sklearn.metrics.pairwise import cosine_similarity

    test_string_good = 'While in service for fuel Engine-31 heard a report of a vehicle fire at building 20190; ' \
                       'Engine-41 was being dispatched to this emergency. Engine-31 lieutenant asked Chief-1 if he ' \
                       'wanted Engine-41 to stand down due to Engine-31 being closer to the incident. Chief-1 approved' \
                       ' and Engine-31 was dispatched to the incident. Firefighters donned all protective structural' \
                       ' fire equipment and responded to the address. Chief 1 also responded to this incident. Crew' \
                       ' arrived on scene, established command, and confirmed there was no active fire. Further' \
                       ' investigation revealed the soldiers working on the vehicle utilized a 10-pound Class ABC' \
                       ' extinguisher to extinguish the fire. Thermal imager camera was utilized by fire crew and' \
                       ' confirmed no hot spots or active fire. Chief-1 arrived on scene and was briefed on the' \
                       ' findings. Soldiers on scene stated the fire started under the crew chief side seat. (Possibly' \
                       ' due to the alternator). They also secured main power to the vehicle to prevent further damage.' \
                       ' Soldiers started complaining of irritation to their eyes and throat; dispatch was advised to' \
                       ' notify EMS and have a unit respond. In the meantime, soldiers were escorted to an eye wash' \
                       ' station inside the warehouse to flush out their eyes. Medic-5 arrived on scene and was briefed' \
                       ' on the patients. Patients refused further medical treatment. Emergency was terminated for' \
                       ' Engine-31, Chief-1, and Medic-5. End report. '
    test_string_related = 'Engine 51 and Medic 5 responded to an MVA on the southbound lanes of Purple Heart Memorial' \
                          ' Freeway (Loop375), reported near the Sgt Major on-ramp. The incident was found and the' \
                          ' correct location was Loop 375 southbound approximately one half mile prior to Barreras' \
                          ' Gate (Exit 28). There was a delayed response due to insufficient information given at time' \
                          ' of dispatch and the distant location. Upon arrival, there was a confirmed 3 vehicle MVA in' \
                          ' the right hand lane. All occupants were assessed for injuries. Only one occupant complained' \
                          ' of pain to his right wrist. Upon Medic 5\'s arrival, patient care was given to transferred.' \
                          ' All the vehicles were fire safe. One vehicle leaked approximately 1/2 gallon of antifreeze' \
                          ' onto the paved road. Absorbent was applied to the leaked fluid. No other hazards were found' \
                          ' at the scene. The emergency was terminated for Engine 51 and left in control of Military' \
                          ' Police.'
    test_string_bad = 'Enter John Bolton, the pugnacious former U.N. ambassador who took over Monday as President' \
                      ' Donald Trump’s national security adviser — the third person to hold the job in barely 14' \
                      ' months. Trump’s selection of Bolton last month set off a guessing game in Washington as to' \
                      ' just how much of an imprint his take-no-prisoners approach to foreign policy will have on' \
                      ' Trump’s team, already beleaguered and exhausted after a tumultuous first year.'
    word_to_embedding = load_lookup()

    test_vector_set = create_vector_set_from_string(test_string_good, word_to_embedding)
    tv_related = create_vector_set_from_string(test_string_related, word_to_embedding)
    test_vector_set_bad = create_vector_set_from_string(test_string_bad, word_to_embedding)
    gq, gr = np.linalg.qr(test_vector_set)
    rq, rr = np.linalg.qr(tv_related)
    bq, br = np.linalg.qr(test_vector_set_bad)

    dist_out_ident = cosine_similarity(gr, gr)
    dist_out_sim = cosine_similarity(gr, rr)
    dist_out_dissim = cosine_similarity(gr, br)

    print('Identity mean:\n{}\n Sim mean:\n{}\nPizza mean:\n{}'.format(dist_out_ident, dist_out_sim, dist_out_dissim))


if __name__ == '__main__':
    main()
