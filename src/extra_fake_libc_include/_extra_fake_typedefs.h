#ifndef DATUM
typedef struct {
	char	*dptr;
	int	dsize;
} datum;
#define DATUM
#endif

// #ifndef _U_INT8_T
// #define _U_INT8_T
// typedef unsigned short                  u_int8_t;
// #endif

#ifndef _U_INT16_T
#define _U_INT16_T
typedef unsigned short                  u_int16_t;
#endif

#ifndef _U_INT32_T
#define _U_INT32_T
typedef unsigned int            u_int32_t;
#endif

#ifndef _U_INT64_T
#define _U_INT64_T
typedef unsigned long long      u_int64_t;
#endif
