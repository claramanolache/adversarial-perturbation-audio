def calculate_frequency_masking_threshold(frame_spectrum, nu, bark_indexer):
    """
    Calculates the global frequency masking threshold theta_x(s, nu)
    for a target frequency 'nu' within a specific audio frame 's'.

    Formula implemented:
    theta_x(s, nu) = 10^Quiet(nu) + sum( 10^T[b(nu), b(i)] )
    """
    # 1. Convert the target frequency (nu) to the Bark scale: b(nu)
    b_nu = bark_indexer.to_bark(nu)

    # 2. Calculate the baseline absolute threshold in quiet: 10^Quiet(nu)
    quiet_nu = bark_indexer.get_quiet_threshold(nu)
    base_threshold = 10 ** quiet_nu

    # 3. Extract the prominent maskers (i) present in this specific frame spectrum (s)
    maskers = bark_indexer.find_maskers(frame_spectrum)

    # 4. Accumulate the spreading effects from all identified maskers
    total_masking_effect = 0.0
    for masker_hz in maskers:
        # Convert masker frequency to Bark scale: b(i)
        b_i = bark_indexer.to_bark(masker_hz)

        # Calculate the masking matrix element: T[b(nu), b(i)]
        t_effect = bark_indexer.spreading_function(b_nu, b_i)

        # Add the power value to the summation
        total_masking_effect += 10 ** t_effect

    # 5. Global threshold is the addition of the baseline and the masked power sum
    theta_x = base_threshold + total_masking_effect

    return theta_x